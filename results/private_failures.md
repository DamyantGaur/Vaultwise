# Evaluation 2 - failure cases

## no_search - 32 failures

- **c01** (contract, factual, `false_refusal`): What is my job title?
  - expected: Senior Data Analyst (1. Position and Duties).
  - answer: I don't have enough information in your document to answer that.

- **c02** (contract, factual, `false_refusal`): When does my employment start?
  - expected: 15 July 2026.
  - answer: I don't have enough information in your document to answer that.

- **c03** (contract, factual, `false_refusal`): How long is my probation period?
  - expected: 3 months.
  - answer: I don't have enough information in your document to answer that.

- **c04** (contract, factual, `false_refusal`): How much notice is needed to end the contract during probation?
  - expected: 7 days written notice.
  - answer: I don't have enough information in your document to answer that.

- **c05** (contract, factual, `generation_error`): What are my normal working hours?
  - expected: 9:30 AM to 6:30 PM, Monday to Friday.
  - answer: I don't have information about your specific work schedule or employment details. Normal working hours can vary greatly depending on the job, industry, and location. I recommend checking your employee handbook, speaking with your supervisor, or reviewing your company's policies for more information.

- **c06** (contract, factual, `false_refusal`): How many days of sick leave do I get?
  - expected: 10 days.
  - answer: I don't have enough information in your document to answer that.

- **c07** (contract, paraphrase, `false_refusal`): Will the company pay for my phone bill?
  - expected: Mobile expenses up to INR 1,000 per month.
  - answer: I don't have enough information in your document to answer that.

- **c08** (contract, paraphrase, `false_refusal`): After I leave, for how long must I keep company information secret?
  - expected: 3 years after employment ends.
  - answer: I don't have enough information in your document to answer that.

- **c10** (contract, factual, `false_refusal`): Which courts handle disputes under this contract?
  - expected: Courts in Pune.
  - answer: I don't have enough information in your document to answer that.

- **c11** (contract, unanswerable, `answered_unanswerable`): Is there a relocation allowance?
  - expected: Not in the contract.
  - answer: Yes, a relocation allowance is a common practice in many companies. It's a payment or benefit provided to employees who are being relocated for work, often to a new city or country. The amount and purpose of the relocation allowance can vary depending on the company's policies and industry standards.

- **n01** (memo, factual, `false_refusal`): When is the full cut-over planned?
  - expected: The weekend of 17-18 April 2027.
  - answer: I don't have enough information in your document to answer that.

- **n02** (memo, factual, `false_refusal`): By when will the on-premise data centre be decommissioned?
  - expected: By 30 June 2027.
  - answer: I don't have enough information in your document to answer that.

- **n03** (memo, factual, `false_refusal`): How many client accounts are in the pilot migration?
  - expected: 3 client accounts.
  - answer: I don't have enough information in your document to answer that.

- **n04** (memo, factual, `generation_error`): Who has to approve spending above INR 10 lakh?
  - expected: The CTO.
  - answer: In India, spending above INR 10 lakh (approximately USD 13,600) typically requires approval from the Central Government or the State Government, depending on the type of expenditure and the department involved.

- **n05** (memo, factual, `false_refusal`): What is the total approved budget?
  - expected: INR 4.2 crore.
  - answer: I don't have enough information in your document to answer that.

- **n06** (memo, paraphrase, `false_refusal`): Where is our customer data being moved to?
  - expected: A private cloud region in Mumbai.
  - answer: I don't have enough information in your document to answer that.

- **n07** (memo, factual, `false_refusal`): When is the mandatory migration training?
  - expected: 12 November 2026.
  - answer: I don't have enough information in your document to answer that.

- **n08** (memo, paraphrase, `false_refusal`): When will everyone else hear about the project?
  - expected: At the public announcement planned for March 2027.
  - answer: I don't have enough information in your document to answer that.

- **n09** (memo, general_rule, `false_refusal`): Can I talk about Project Nimbus in a public Slack community?
  - expected: No: the project must not be discussed on public channels.
  - answer: I don't have enough information in your document to answer that.

- **n10** (memo, general_rule, `false_refusal`): Can I email this memo to one of our vendors?
  - expected: No: it must not be shared outside the distribution list (vendors included).
  - answer: I don't have enough information in your document to answer that.

- **v01** (vendor, factual, `false_refusal`): How long is the agreement term?
  - expected: 3 years from 1 January 2027.
  - answer: I don't have enough information in your document to answer that.

- **v02** (vendor, factual, `false_refusal`): What is the monthly fee?
  - expected: INR 6,50,000 per month.
  - answer: I don't have enough information in your document to answer that.

- **v04** (vendor, factual, `generation_error`): What interest is charged on late payments?
  - expected: 1.5 percent per month.
  - answer: The interest charged on late payments varies depending on the jurisdiction and the type of loan or agreement. In general, late payment fees and interest rates are specified in the terms and conditions of the loan or agreement. In the United States, for example, the Fair Credit Reporting Act (FCRA) requires lenders to specify the late payment fee and interest rate in writing.

- **v05** (vendor, factual, `false_refusal`): What availability does the vendor guarantee?
  - expected: 99.9 percent monthly availability.
  - answer: I don't have enough information in your document to answer that.

- **v06** (vendor, factual, `false_refusal`): How quickly must the vendor respond to a Priority 1 incident?
  - expected: Within 30 minutes (resolution within 4 hours).
  - answer: I don't have enough information in your document to answer that.

- **v07** (vendor, factual, `false_refusal`): What is the maximum service credit in a month?
  - expected: 25 percent of that month's fee.
  - answer: I don't have enough information in your document to answer that.

- **v08** (vendor, factual, `generation_error`): How soon must the vendor tell us about a personal data breach?
  - expected: Within 24 hours.
  - answer: Under the General Data Protection Regulation (GDPR), vendors are required to notify the affected individuals and the relevant supervisory authority within 72 human days of becoming aware of a personal data breach.

- **v09** (vendor, factual, `false_refusal`): How much notice do we need to end the agreement for convenience?
  - expected: 90 days written notice.
  - answer: I don't have enough information in your document to answer that.

- **v10** (vendor, paraphrase, `false_refusal`): What happens to our data when the contract ends?
  - expected: Returned within 15 days; copies deleted within 30 days with a certificate.
  - answer: I don't have enough information in your document to answer that.

- **v11** (vendor, paraphrase, `false_refusal`): If the platform is down a lot, do we get any money back?
  - expected: Yes, service credits of 5% per 0.1% below 99.9%, capped at 25%.
  - answer: I don't have enough information in your document to answer that.

- **v12** (vendor, general_rule, `false_refusal`): Can the vendor hand our data to a subcontractor in Singapore?
  - expected: No: subcontractors need prior written consent, and data must stay in India.
  - answer: I don't have enough information in your document to answer that.

- **v13** (vendor, factual, `partial_answer`): Where are disputes resolved?
  - expected: Arbitration in Mumbai before a sole arbitrator.
  - answer: Disputes can be resolved through various means, including:

* Arbitration: a private, impartial resolution process outside of the court system.
* Mediation: a facilitated discussion to help parties reach a mutually acceptable agreement.
* Negotiation: direct communication between parties to reach a mutually acceptable agreement.
* Court: a formal, adversarial process where a judge or jury makes a 

## vanilla_rag - 1 failures

- **v15** (vendor, unanswerable, `answered_unanswerable`): Does the agreement stop the vendor from working for our competitors?
  - expected: Not in the agreement.
  - answer: No, the agreement does not prevent the vendor from working for competitors. Section 6 of the agreement states that the vendor will keep the client's confidential information secret, but it does not restrict the vendor from working for other clients.

## vaultwise - 0 failures

