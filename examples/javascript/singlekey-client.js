/**
 * SingleKey API JavaScript/Node.js Client
 *
 * A complete JavaScript client for the SingleKey Screening API.
 *
 * Installation:
 *   npm install axios
 *
 * Usage:
 *   const SingleKeyClient = require('./singlekey-client');
 *   const client = new SingleKeyClient('your_api_token');
 */

const axios = require('axios');

// Environment constants
const Environment = {
  PRODUCTION: 'https://platform.singlekey.com',
  SANDBOX: 'https://sandbox.singlekey.com'
};

// Custom error classes
class SingleKeyError extends Error {
  constructor(message, errors = []) {
    super(message);
    this.name = 'SingleKeyError';
    this.errors = errors;
  }
}

class AuthenticationError extends SingleKeyError {
  constructor(message) {
    super(message);
    this.name = 'AuthenticationError';
  }
}

class ValidationError extends SingleKeyError {
  constructor(message, errors) {
    super(message, errors);
    this.name = 'ValidationError';
  }
}

class NotFoundError extends SingleKeyError {
  constructor(message) {
    super(message);
    this.name = 'NotFoundError';
  }
}

/**
 * SingleKey API Client
 *
 * @example
 * const client = new SingleKeyClient('your_api_token');
 *
 * const result = await client.createScreening({
 *   landlord: {
 *     firstName: 'John',
 *     lastName: 'Smith',
 *     email: 'john@example.com'
 *   },
 *   tenant: {
 *     firstName: 'Jane',
 *     lastName: 'Doe',
 *     email: 'jane@example.com',
 *     phone: '5551234567',
 *     dob: { year: 1990, month: 6, day: 15 },
 *     address: '123 Main St, Toronto, ON, Canada, M5V 1A1',
 *     sin: '123456789'
 *   }
 * });
 */
class SingleKeyClient {
  /**
   * Create a new SingleKey client
   * @param {string} apiToken - Your API token
   * @param {Object} options - Configuration options
   * @param {string} options.environment - PRODUCTION or SANDBOX
   * @param {number} options.timeout - Request timeout in ms
   */
  constructor(apiToken, options = {}) {
    this.apiToken = apiToken;
    this.baseUrl = options.environment || Environment.PRODUCTION;
    this.timeout = options.timeout || 30000;

    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: this.timeout,
      headers: {
        'Authorization': `Token ${apiToken}`,
        'Content-Type': 'application/json'
      }
    });
  }

  /**
   * Make an API request
   * @private
   */
  async _request(method, endpoint, data = null, params = null) {
    try {
      const response = await this.client.request({
        method,
        url: endpoint,
        data,
        params
      });

      const result = response.data;

      // Check for API-level errors
      if (result.success === false && result.errors) {
        throw new ValidationError(
          result.detail || 'Validation failed',
          result.errors
        );
      }

      return result;

    } catch (error) {
      if (error instanceof SingleKeyError) {
        throw error;
      }

      if (error.response) {
        const status = error.response.status;

        if (status === 401) {
          throw new AuthenticationError('Invalid API token');
        }

        if (status === 404) {
          throw new NotFoundError('Resource not found');
        }

        const data = error.response.data;
        if (data && data.errors) {
          throw new ValidationError(data.detail || 'Request failed', data.errors);
        }

        throw new SingleKeyError(`Request failed with status ${status}`);
      }

      if (error.code === 'ECONNABORTED') {
        throw new SingleKeyError('Request timed out');
      }

      throw new SingleKeyError(error.message);
    }
  }

  /**
   * Create a new screening request
   * @param {Object} options - Screening options
   * @param {Object} options.landlord - Landlord information
   * @param {Object} options.tenant - Tenant information
   * @param {Object} options.property - Property information (optional)
   * @param {boolean} options.runNow - Process immediately (default true)
   * @param {boolean} options.tenantPays - Tenant provides payment
   * @param {string} options.callbackUrl - Webhook URL
   * @returns {Promise<Object>} Screening result with purchase_token
   */
  async createScreening({
    landlord,
    tenant,
    property = null,
    runNow = true,
    tenantPays = false,
    callbackUrl = null,
    externalDealId = null
  }) {
    const payload = {
      external_customer_id: landlord.externalId || `ll-${landlord.email}`,
      external_tenant_id: tenant.externalId || `tn-${tenant.email}`,
      run_now: runNow,
      tenant_pays: tenantPays,

      // Landlord info
      ll_first_name: landlord.firstName,
      ll_last_name: landlord.lastName,
      ll_email: landlord.email,

      // Tenant info
      ten_first_name: tenant.firstName,
      ten_last_name: tenant.lastName,
      ten_email: tenant.email,
      ten_tel: tenant.phone,
      ten_dob_year: tenant.dob.year,
      ten_dob_month: tenant.dob.month,
      ten_dob_day: tenant.dob.day,
      ten_address: tenant.address,
      ten_sin: tenant.sin
    };

    // Optional fields
    if (landlord.phone) payload.ll_tel = landlord.phone;
    if (tenant.middleName) payload.ten_middle_name = tenant.middleName;
    if (tenant.employer) payload.ten_employer = tenant.employer;
    if (tenant.jobTitle) payload.ten_job_title = tenant.jobTitle;
    if (tenant.annualIncome) payload.ten_annual_income = tenant.annualIncome;

    if (property) {
      payload.purchase_address = property.address;
      if (property.rent) payload.purchase_rent = property.rent;
      if (property.unit) payload.purchase_unit = property.unit;
    }

    if (callbackUrl) payload.callback_url = callbackUrl;
    if (externalDealId) payload.external_deal_id = externalDealId;

    return this._request('POST', '/api/request', payload);
  }

  /**
   * Create a form-based screening request
   * @param {Object} options - Form request options
   * @returns {Promise<Object>} Result with form_url
   */
  async createFormRequest({
    landlord,
    tenantEmail,
    tenantFirstName = null,
    tenantLastName = null,
    propertyAddress = null,
    tenantForm = false,
    callbackUrl = null
  }) {
    const payload = {
      external_customer_id: landlord.externalId || `ll-${landlord.email}`,
      external_tenant_id: `tn-${tenantEmail}`,

      ll_first_name: landlord.firstName,
      ll_last_name: landlord.lastName,
      ll_email: landlord.email,

      ten_email: tenantEmail
    };

    if (landlord.phone) payload.ll_tel = landlord.phone;
    if (tenantFirstName) payload.ten_first_name = tenantFirstName;
    if (tenantLastName) payload.ten_last_name = tenantLastName;

    if (tenantForm) {
      payload.tenant_form = true;
      if (propertyAddress) payload.purchase_address = propertyAddress;
    }

    if (callbackUrl) payload.callback_url = callbackUrl;

    return this._request('POST', '/api/request', payload);
  }

  /**
   * Get screening report
   * @param {string} purchaseToken - Token from createScreening
   * @returns {Promise<Object>} Report data or status
   */
  async getReport(purchaseToken) {
    return this._request('GET', `/api/report/${purchaseToken}`);
  }

  /**
   * Get applicant information
   * @param {string} purchaseToken - Token from createScreening
   * @param {Object} options - Query options
   * @returns {Promise<Object>} Applicant data
   */
  async getApplicant(purchaseToken, { detailed = false, showCreditScore = false } = {}) {
    const params = {};
    if (detailed) params.detailed = 'true';
    if (showCreditScore) params.show_credit_score = 'true';

    return this._request('GET', `/api/applicant/${purchaseToken}`, null, params);
  }

  /**
   * Validate screening for errors
   * @param {string} screeningId - Screening ID to validate
   * @returns {Promise<Object>} Validation result
   */
  async validateScreening(screeningId) {
    return this._request('POST', `/api/purchase_errors/${screeningId}`);
  }

  /**
   * Download report as PDF
   * @param {string} purchaseToken - Token from createScreening
   * @returns {Promise<Buffer>} PDF file buffer
   */
  async downloadPdf(purchaseToken) {
    const response = await this.client.get(`/api/report_pdf/${purchaseToken}`, {
      responseType: 'arraybuffer'
    });

    return Buffer.from(response.data);
  }

  /**
   * Poll until report is ready
   * @param {string} purchaseToken - Token from createScreening
   * @param {Object} options - Polling options
   * @returns {Promise<Object>} Completed report
   */
  async waitForReport(purchaseToken, { timeout = 300000, pollInterval = 10000 } = {}) {
    const startTime = Date.now();

    while (Date.now() - startTime < timeout) {
      const report = await this.getReport(purchaseToken);

      if (report.success && report.singlekey_score) {
        return report;
      }

      console.log(`Status: ${report.detail || 'Processing...'}`);
      await new Promise(resolve => setTimeout(resolve, pollInterval));
    }

    throw new SingleKeyError('Timeout waiting for report');
  }
}

// Export for Node.js
module.exports = {
  SingleKeyClient,
  SingleKeyError,
  AuthenticationError,
  ValidationError,
  NotFoundError,
  Environment
};

// Example usage
async function main() {
  const client = new SingleKeyClient('your_api_token', {
    environment: Environment.SANDBOX
  });

  try {
    // Create screening
    const result = await client.createScreening({
      landlord: {
        externalId: 'landlord-123',
        firstName: 'John',
        lastName: 'Smith',
        email: 'john@example.com',
        phone: '5551234567'
      },
      tenant: {
        externalId: 'tenant-456',
        firstName: 'Jane',
        lastName: 'Doe',
        email: 'jane@example.com',
        phone: '5559876543',
        dob: { year: 1990, month: 6, day: 15 },
        address: '456 Oak Ave, Toronto, ON, Canada, M5V 2B3',
        sin: '123456789'
      },
      property: {
        address: '123 Main St, Toronto, ON, Canada, M5V 1A1',
        rent: 2000
      },
      callbackUrl: 'https://yoursite.com/webhooks/singlekey'
    });

    console.log(`Screening created: ${result.purchase_token}`);

    // Wait for report
    const report = await client.waitForReport(result.purchase_token);

    console.log(`SingleKey Score: ${report.singlekey_score}`);
    console.log(`Report URL: ${report.report_url}`);

    // Download PDF
    const fs = require('fs');
    const pdfBuffer = await client.downloadPdf(result.purchase_token);
    fs.writeFileSync('screening_report.pdf', pdfBuffer);
    console.log('PDF saved to screening_report.pdf');

  } catch (error) {
    if (error instanceof ValidationError) {
      console.error('Validation failed:', error.message);
      error.errors.forEach(err => console.error(`  - ${err}`));
    } else {
      console.error('API error:', error.message);
    }
  }
}

// Run example if executed directly
if (require.main === module) {
  main();
}
