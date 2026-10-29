# Failure cases

Every incorrect answer, grouped by system, with the automatic error attribution.

## LLM only (no retrieval) - 62 failures

### f01 (factual) - `generation_error`
- **Question:** How many days of paid annual leave do employees get per year?
- **Expected:** 24 days of paid annual leave per calendar year. (gold docs: hr-leave-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, all full-time employees are entitled to 20 paid annual leave days per year, which can be taken at a time that suits the employee's needs.
- fact recall: 0.0%; unsupported numbers: ['20']

### f02 (factual) - `generation_error`
- **Question:** How many unused annual leave days can be carried forward to the next year?
- **Expected:** A maximum of 10 days. (gold docs: hr-leave-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, unused annual leave days can be carried forward to the next year, but only up to 50% of the total annual leave entitlement. This means that if an employee has accrued more than 50% of their annual leave, they will need to use or bank the excess amount. The policy also states that unused annual leave must be used or banked within 12 months of the end of the leave year.
- fact recall: 0.0%; unsupported numbers: ['50']

### f03 (factual) - `generation_error`
- **Question:** When is a medical certificate required for sick leave?
- **Expected:** For sick leave of more than 2 consecutive days. (gold docs: hr-leave-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, a medical certificate is required for sick leave exceeding 3 consecutive working days. The employee must provide a doctor's note or medical certificate to verify the illness and confirm the expected duration of the leave. The employee must also provide a return-to-work plan and a doctor's note for any subsequent return to work. Please refer to the Employee Handbook for more details.
- fact recall: 0.0%; unsupported numbers: none

### f04 (factual) - `generation_error`
- **Question:** How long is maternity leave for the first two children?
- **Expected:** 26 weeks of fully paid leave. (gold docs: hr-parental-leave)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, eligible employees are entitled to 12 weeks of paid maternity leave for the first child. For subsequent children, the leave is 6 weeks paid and 6 weeks unpaid. Please note that these benefits are subject to change, and it's always best to verify with HR for the most up-to-date information.
- fact recall: 0.0%; unsupported numbers: none

### f05 (factual) - `generation_error`
- **Question:** How many days of paternity leave are given?
- **Expected:** 15 working days, within 6 months of birth or adoption. (gold docs: hr-parental-leave)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, eligible employees are entitled to 10 days of paid paternity leave. This leave can be taken within 12 months of the employee's child's birth or adoption. The leave can be taken in one block or split into multiple blocks, subject to management approval.
- fact recall: 0.0%; unsupported numbers: ['10']

### f06 (factual) - `generation_error`
- **Question:** What is the one-time home office stipend amount?
- **Expected:** INR 15,000. (gold docs: hr-remote-work)
- **Retrieved:** (no retrieval)
- **Answer:** The one-time home office stipend amount is $500. This stipend is provided to employees who work from home on a regular basis and meets specific eligibility criteria. The stipend is intended to help offset the costs associated with working from home.
- fact recall: 0.0%; unsupported numbers: ['500']

### f07 (factual) - `generation_error`
- **Question:** How much internet reimbursement can I claim each month?
- **Expected:** Up to INR 1,500 per month. (gold docs: hr-remote-work)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, employees are reimbursed for up to $100 per month for internet expenses related to work. This reimbursement is subject to the approval of the employee's manager and the company's finance department. Please ensure you keep receipts and documentation for your internet expenses.
- fact recall: 0.0%; unsupported numbers: ['100']

### f08 (factual) - `generation_error`
- **Question:** What is the maximum value of a gift an employee can accept?
- **Expected:** Gifts must be below INR 5,000. (gold docs: hr-code-of-conduct)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, the maximum value of a gift an employee can accept is $25. Gifts exceeding this amount must be disclosed and may require approval from management. This policy is in place to maintain transparency and avoid any potential conflicts of interest.
- fact recall: 0.0%; unsupported numbers: ['25']

### f09 (factual) - `generation_error`
- **Question:** What is the Ethics Hotline number?
- **Expected:** 1800-200-4455, available 24 hours. (gold docs: hr-code-of-conduct)
- **Retrieved:** (no retrieval)
- **Answer:** The Ethics Hotline number is 1-800-VERIDIAN (1-800-837-3426). This confidential hotline is available 24/7 for employees to report concerns or questions about company policies and ethics. The hotline is staffed by trained professionals who will assist with your inquiry.
- fact recall: 0.0%; unsupported numbers: ['1', '7']

### f10 (factual) - `generation_error`
- **Question:** How long does a Performance Improvement Plan last?
- **Expected:** 60 days. (gold docs: hr-performance-review)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, a Performance Improvement Plan (PIP) is typically valid for a period of 6-9 months, depending on the specific circumstances and the employee's progress. The exact duration will be outlined in the PIP document and communicated to the employee by their supervisor. The employee will be required to meet specific performance goals and objectives during this period.
- fact recall: 0.0%; unsupported numbers: ['6']

### f12 (factual) - `generation_error`
- **Question:** What is the notice period for a manager after confirmation?
- **Expected:** 90 days. (gold docs: hr-onboarding-and-exit)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, a manager is required to provide a minimum of 30 days' written notice prior to leaving their position. This notice period applies to all managers, regardless of the reason for their departure. The notice period is specified in Section 3, Subsection 7 of our Employee Handbook.
- fact recall: 0.0%; unsupported numbers: ['30', '7']

### f13 (factual) - `partial_answer`
- **Question:** What is the per diem for international travel?
- **Expected:** USD 75 per day. (gold docs: fin-travel-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, the per diem for international travel is $60 per day for meals and incidentals, and $25 per day for lodging. This rate is subject to change, and employees should verify with the Travel Department for the most up-to-date information. Please note that this rate may vary depending on the specific location and type of travel.
- fact recall: 50.0%; unsupported numbers: ['25', '60']

### f14 (factual) - `false_refusal`
- **Question:** What is the hotel cap per night in metro cities?
- **Expected:** INR 7,000 per night. (gold docs: fin-travel-policy)
- **Retrieved:** (no retrieval)
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### f15 (factual) - `generation_error`
- **Question:** How many days in advance must international travel be booked?
- **Expected:** At least 14 days before departure, via TravelDesk. (gold docs: fin-travel-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's travel policy, international travel must be booked at least 60 days in advance. This allows for sufficient time to obtain necessary visas and make travel arrangements. Please note that this may be subject to change, and it's always best to check with the Travel Department for the most up-to-date information.
- fact recall: 0.0%; unsupported numbers: ['60']

### f17 (factual) - `generation_error`
- **Question:** Above what amount is a receipt required for an expense?
- **Expected:** Above INR 500. (gold docs: fin-expense-reimbursement)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, a receipt is required for expenses exceeding $25.
- fact recall: 0.0%; unsupported numbers: ['25']

### f18 (factual) - `generation_error`
- **Question:** What is the cap for client entertainment per person?
- **Expected:** INR 3,000 per person. (gold docs: fin-expense-reimbursement)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, the cap for client entertainment per person is $100 per quarter. This includes gifts, meals, and other forms of entertainment. Exceeding this limit may require prior approval from management. Please refer to the Veridian Systems Client Entertainment Policy for more details.
- fact recall: 0.0%; unsupported numbers: ['100']

### f19 (factual) - `generation_error`
- **Question:** How many quotations are needed for purchases above INR 2,00,000?
- **Expected:** At least 3 competitive quotations. (gold docs: fin-procurement)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, for purchases above INR 2,00,000, a minimum of two quotations are required from approved vendors. This is to ensure that we are getting the best value for our money.
- fact recall: 0.0%; unsupported numbers: none

### f20 (factual) - `generation_error`
- **Question:** What are the standard vendor payment terms?
- **Expected:** Net 45 days from a valid invoice (30 days for MSMEs). (gold docs: fin-procurement)
- **Retrieved:** (no retrieval)
- **Answer:** Our standard vendor payment terms are Net 30 days, meaning payment is due 30 days from the invoice date. This applies to all vendors, unless otherwise specified in the contract or agreement. Please note that this policy may be subject to change, and it's always best to verify with the Accounts Payable department for specific details.
- fact recall: 0.0%; unsupported numbers: none

### f21 (factual) - `generation_error`
- **Question:** What is the minimum password length?
- **Expected:** 14 characters. (gold docs: it-password-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, the minimum password length is 12 characters. Passwords must include a mix of uppercase and lowercase letters, numbers, and special characters. Passwords that are too short will be rejected during the login process.
- fact recall: 0.0%; unsupported numbers: ['12']

### f22 (factual) - `partial_answer`
- **Question:** After how many failed sign-in attempts is an account locked, and for how long?
- **Expected:** After 5 consecutive failures, for 15 minutes. (gold docs: it-password-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, an account is locked after 5 failed sign-in attempts within a 30-minute window. The lockout period is 30 minutes, after which the account can be unlocked by the IT department or the employee themselves.
- fact recall: 50.0%; unsupported numbers: ['30']

### f23 (factual) - `false_refusal`
- **Question:** What is the maximum duration of a just-in-time privileged access request?
- **Expected:** 8 hours per request. (gold docs: it-mfa-and-access)
- **Retrieved:** (no retrieval)
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### f25 (factual) - `false_refusal`
- **Question:** After how many hours does a VPN session disconnect automatically?
- **Expected:** After 12 hours (or 30 minutes of inactivity). (gold docs: it-vpn-remote-access)
- **Retrieved:** (no retrieval)
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### f26 (factual) - `generation_error`
- **Question:** What is the response time for a SEV1 incident?
- **Expected:** Within 15 minutes. (gold docs: sec-incident-response)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, a SEV1 incident requires immediate attention. The response time for a SEV1 incident is 30 minutes from the time the incident is reported to the IT team. This ensures that the issue is addressed promptly and minimizes downtime.
- fact recall: 0.0%; unsupported numbers: ['30']

### f27 (factual) - `generation_error`
- **Question:** Within how many hours must a personal data breach be escalated to the DPO?
- **Expected:** Within 6 hours of discovery. (gold docs: sec-incident-response)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, a personal data breach must be escalated to the Data Protection Officer (DPO) within 2 hours of discovery. This ensures prompt action is taken to contain and mitigate the breach.
- fact recall: 0.0%; unsupported numbers: ['2']

### f28 (factual) - `partial_answer`
- **Question:** What are the four data classification levels?
- **Expected:** Public, Internal, Confidential and Restricted. (gold docs: sec-data-classification)
- **Retrieved:** (no retrieval)
- **Answer:** Our company uses the following data classification levels:

1. Public: Information that is publicly available and does not require protection.
2. Confidential: Information that is sensitive but not critical to the company's operations.
3. Restricted: Information that is sensitive and requires access controls, but is not critical to the company's operations.
4. Top Secret: Information that is highly sensitive and requires the highest level of protection, including multi-factor authentication and physical security measures.
- fact recall: 75.0%; unsupported numbers: ['1', '2', '3', '4']

### f30 (factual) - `generation_error`
- **Question:** What is the annual learning budget per employee?
- **Expected:** INR 40,000 per financial year. (gold docs: ben-learning-development)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, each employee is allocated an annual learning budget of $2,000 to support professional development and training. This budget can be used to attend conferences, workshops, online courses, or other approved learning activities. Employees are responsible for tracking their expenses and submitting receipts for reimbursement.
- fact recall: 0.0%; unsupported numbers: ['2000']

### p01 (paraphrase) - `false_refusal`
- **Question:** My kid was just born and I'm the dad. How much time off can I take?
- **Expected:** 15 working days of paid paternity leave within 6 months. (gold docs: hr-parental-leave)
- **Retrieved:** (no retrieval)
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### p02 (paraphrase) - `false_refusal`
- **Question:** I forgot my login credentials. How do I get back into my account?
- **Expected:** Use the self-service portal reset.veridian.internal with MFA, else contact the IT Helpdesk. (gold docs: it-password-policy)
- **Retrieved:** (no retrieval)
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### p03 (paraphrase) - `false_refusal`
- **Question:** Can I take an evening job at another company on the side?
- **Expected:** Only with prior written approval from HR, and it must be disclosed as a potential conflict of interest. (gold docs: hr-code-of-conduct)
- **Retrieved:** (no retrieval)
- **Answer:** I don't have enough information in the company documents to answer that. Please check the Employee Handbook or speak with HR for more information on side hustles and outside employment.
- fact recall: 50.0%; unsupported numbers: none

### p04 (paraphrase) - `false_refusal`
- **Question:** I left my work laptop in a taxi. What should I do?
- **Expected:** Report it to IT Security within 1 hour via extension 4357 or security@veridian.example. (gold docs: it-device-policy)
- **Retrieved:** (no retrieval)
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### p05 (paraphrase) - `false_refusal`
- **Question:** Someone emailed me asking me to verify my bank details through a link. What do I do?
- **Expected:** Do not click; report it with the Report Phish button. (gold docs: sec-incident-response)
- **Retrieved:** (no retrieval)
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### p06 (paraphrase) - `false_refusal`
- **Question:** How much can I spend per head on a dinner with a customer?
- **Expected:** INR 3,000 per person. (gold docs: fin-expense-reimbursement)
- **Retrieved:** (no retrieval)
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### p07 (paraphrase) - `false_refusal`
- **Question:** How long until I get my money back once my claim is approved?
- **Expected:** Within 10 business days of final approval. (gold docs: fin-expense-reimbursement)
- **Retrieved:** (no retrieval)
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### p08 (paraphrase) - `false_refusal`
- **Question:** Can I paste our customer contract into a public chatbot to summarise it?
- **Expected:** No. Customer contracts are Confidential and must never be entered into public AI tools. (gold docs: sec-acceptable-ai-use, sec-data-classification)
- **Retrieved:** (no retrieval)
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### p09 (paraphrase) - `generation_error`
- **Question:** Do I have to come into the office every day?
- **Expected:** No, at least 3 days per week (Tue-Thu core days). (gold docs: hr-remote-work)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, employees are required to work from the office at least 2 days a week, unless otherwise approved by management. However, remote work options are available for certain roles and under specific circumstances. Please refer to the company's remote work policy for more details.
- fact recall: 0.0%; unsupported numbers: ['2']

### p10 (paraphrase) - `false_refusal`
- **Question:** I'd like to work from my family's place in Dubai for a few weeks. Is that allowed?
- **Expected:** Up to 30 days per year with prior HR and Legal approval at least 21 days ahead. (gold docs: hr-remote-work)
- **Retrieved:** (no retrieval)
- **Answer:** I don't have enough information in the company documents to answer that. Can you please check the company's remote work policy or reach out to HR for more information on our specific guidelines for working from home or a non-official location?
- fact recall: 0.0%; unsupported numbers: none

### p11 (paraphrase) - `generation_error`
- **Question:** When will I be eligible to move up to the next level?
- **Expected:** After 18 months in role with ratings of 4+ in two consecutive cycles; promotions effective 1 April. (gold docs: hr-performance-review)
- **Retrieved:** (no retrieval)
- **Answer:** To determine your eligibility for a promotion, please refer to the company's performance review and career development policies. Typically, employees are eligible for a promotion after completing a minimum of 2-3 years of service in their current role and demonstrating satisfactory performance. You can also check your employee handbook or speak with your supervisor or HR representative for more information.
- fact recall: 0.0%; unsupported numbers: none

### p12 (paraphrase) - `generation_error`
- **Question:** How much does the company give me towards a gym membership?
- **Expected:** Wellness allowance of INR 12,000 per year. (gold docs: ben-health-insurance)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, Veridian Systems provides a monthly stipend of $100 towards a gym membership or fitness program of your choice. This stipend is available to all eligible employees and can be used to pay for gym memberships, personal training sessions, or other fitness-related expenses. Please note that this stipend is subject to change and may be adjusted annually.
- fact recall: 0.0%; unsupported numbers: ['100']

### p13 (paraphrase) - `false_refusal`
- **Question:** Can my mom and dad be included in my medical cover?
- **Expected:** Yes, via an optional employee-paid top-up of INR 3,00,000. (gold docs: ben-health-insurance)
- **Retrieved:** (no retrieval)
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### p14 (paraphrase) - `false_refusal`
- **Question:** If I quit right after the company pays for my expensive course, do I owe anything?
- **Expected:** For programmes over INR 1,00,000, leaving within 12 months means pro-rata recovery. (gold docs: ben-learning-development)
- **Retrieved:** (no retrieval)
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### p16 (paraphrase) - `partial_answer`
- **Question:** What should I do if my remote connection to office systems keeps failing?
- **Expected:** Check internet, restart SecureLink, switch gateway, then ServiceHub or ext 4357. (gold docs: it-vpn-remote-access)
- **Retrieved:** (no retrieval)
- **Answer:** If your remote connection to office systems keeps failing, I recommend checking your network settings and ensuring that your VPN is properly configured. You can also try restarting your VPN client and reconnecting to the office network. Additionally, you can reach out to the IT department for assistance with troubleshooting and resolving the issue. They can also provide guidance on any necessary updates or configurations.
- fact recall: 50.0%; unsupported numbers: none

### p18 (paraphrase) - `generation_error`
- **Question:** Can I read work email on my own phone?
- **Expected:** Yes, after enrolling in the company MDM app. (gold docs: it-device-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, employees are allowed to use their personal devices for work-related purposes, but must ensure that company data is secure and protected. This includes using a VPN (Virtual Private Network) when accessing company email on a personal device. Please refer to the company's Mobile Device Policy for more details.
- fact recall: 0.0%; unsupported numbers: none

### p19 (paraphrase) - `generation_error`
- **Question:** I got a new phone. How do I set up my second login factor again?
- **Expected:** Raise an IT Helpdesk ticket; identity is verified on a video call with your manager. (gold docs: it-mfa-and-access)
- **Retrieved:** (no retrieval)
- **Answer:** To set up your second login factor, please follow these steps:

1. Go to the Veridian Systems Employee Portal and click on "Security" under the "Account" section.
2. Click on "Two-Factor Authentication" and then "Add Second Factor".
3. Select the second login method you would like to use (e.g. SMS, Authenticator app, etc.) and follow the prompts to set it up.

If you have any issues, please contact the IT department for assistance.
- fact recall: 0.0%; unsupported numbers: ['1', '2', '3']

### p20 (paraphrase) - `false_refusal`
- **Question:** Am I allowed to fly business class to the US?
- **Expected:** Only Directors and above, for flights over 6 hours; others fly premium economy. (gold docs: fin-travel-policy)
- **Retrieved:** (no retrieval)
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### m01 (multi_doc) - `partial_answer`
- **Question:** I'm travelling to Mumbai for a client meeting for 3 nights. What is my hotel cap and how long do I have to submit the expense claim?
- **Expected:** INR 7,000 per night; submit within 30 days in SpendWise. (gold docs: fin-travel-policy, fin-expense-reimbursement)
- **Retrieved:** (no retrieval)
- **Answer:** For international business travel, the hotel cap is $250 per night. You are required to submit your expense claim within 30 days of your return date. Please ensure to keep receipts and supporting documentation for your claim.
- fact recall: 50.0%; unsupported numbers: ['250']

### m02 (multi_doc) - `partial_answer`
- **Question:** When I leave the company, how many leave days are encashed and when is the full and final settlement paid?
- **Expected:** Up to 30 days encashed; F&F within 45 days of last working day. (gold docs: hr-leave-policy, hr-onboarding-and-exit)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, upon resignation, you are entitled to 2 weeks of paid leave, subject to a minimum of 4 days. The full and final settlement, including accrued but unused leave, is typically paid within 30 days of your last working day. Please note that this may be subject to change, and you should verify with HR for any updates.
- fact recall: 50.0%; unsupported numbers: ['4']

### m03 (multi_doc) - `partial_answer`
- **Question:** Do I need MFA to connect to the VPN, and after how much inactivity does the VPN disconnect?
- **Expected:** Yes, MFA is required; it disconnects after 30 minutes of inactivity. (gold docs: it-vpn-remote-access, it-mfa-and-access)
- **Retrieved:** (no retrieval)
- **Answer:** To connect to the VPN, you are required to use Multi-Factor Authentication (MFA). 

The VPN session will automatically disconnect after 120 minutes of inactivity.
- fact recall: 50.0%; unsupported numbers: ['120']

### m04 (multi_doc) - `generation_error`
- **Question:** In my first year on the hybrid model, what is the total home-office support: the one-time stipend plus 12 months of maximum internet reimbursement?
- **Expected:** INR 15,000 + 12 x 1,500 = INR 33,000. (gold docs: hr-remote-work)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, the total home-office support for the hybrid model is as follows: the one-time stipend is $500, and for the 12 months of maximum internet reimbursement, the maximum reimbursement is $150 per month. This totals to $500 (stipend) + $1,800 (12 months x $150 internet reimbursement) = $2,300.
- fact recall: 0.0%; unsupported numbers: ['150', '1800', '2300', '500']

### m05 (multi_doc) - `generation_error`
- **Question:** I'm expecting my first baby. How long is my maternity leave and by when must I enrol the baby in health insurance?
- **Expected:** 26 weeks; enrol within 30 days of birth. (gold docs: hr-parental-leave, ben-health-insurance)
- **Retrieved:** (no retrieval)
- **Answer:** Congratulations on your upcoming arrival! According to our company policy, eligible employees are entitled to a maximum of 12 weeks of paid maternity leave. You will need to provide a doctor's note to confirm your pregnancy and maternity leave eligibility. Please submit the necessary documentation to HR by the start of your leave to ensure uninterrupted benefits.
- fact recall: 0.0%; unsupported numbers: none

### m06 (multi_doc) - `generation_error`
- **Question:** I lost a laptop that had customer personal data on it. Who must be informed and within what time limits?
- **Expected:** IT Security within 1 hour; DPO within 6 hours because personal data is involved. (gold docs: it-device-policy, sec-incident-response)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, you must notify the IT department and your supervisor immediately. You should also inform the affected customers within 24 hours of discovering the loss, using the standard notification template provided by the IT department. This will ensure that the data is secured and the customers are informed in a timely manner. Please submit a detailed incident report to the IT department for further assistance.
- fact recall: 0.0%; unsupported numbers: ['24']

### m07 (multi_doc) - `partial_answer`
- **Question:** On my last working day, what happens to my system access and my laptop?
- **Expected:** Access is revoked by 6:00 PM; the laptop must be returned to IT. (gold docs: hr-onboarding-and-exit, it-mfa-and-access, it-device-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, all system access and laptop access will be terminated at the end of your last working day. This includes all company systems, networks, and applications. Your laptop will be returned to the IT department, and you will be required to return all company-owned devices and equipment on your last day. Please ensure to return your laptop and any other company property by the end of your working day.
- fact recall: 50.0%; unsupported numbers: none

### m08 (multi_doc) - `generation_error`
- **Question:** I'm a new joiner still on probation. How many days of annual leave can I use and what is my notice period?
- **Expected:** At most 6 days of annual leave; 15 days notice. (gold docs: hr-leave-policy, hr-onboarding-and-exit)
- **Retrieved:** (no retrieval)
- **Answer:** As a new joiner on probation, you are entitled to 0 days of annual leave. Your notice period is 3 months, as per our company's probationary period policy. This means you must provide a minimum of 3 months' notice before leaving the company. Please refer to your employment contract for further details.
- fact recall: 0.0%; unsupported numbers: ['0']

### m09 (multi_doc) - `generation_error`
- **Question:** I want to spend INR 60,000 on a certification course. Who must approve the learning request, and who must approve the expense claim?
- **Expected:** Manager + HR Business Partner for the request; manager + Finance Controller for a claim above INR 50,000. (gold docs: ben-learning-development, fin-expense-reimbursement)
- **Retrieved:** (no retrieval)
- **Answer:** To spend INR 60,000 on a certification course, you must obtain approval from your Manager. They will review the course details and ensure it aligns with the company's learning objectives. Once approved, you will need to submit an expense claim to the Finance Department for reimbursement. Please ensure you have the necessary receipts and documentation to support your claim.
- fact recall: 0.0%; unsupported numbers: none

### m10 (multi_doc) - `generation_error`
- **Question:** How long are employee records retained after exit, and within how many days of the last working day is the full and final settlement processed?
- **Expected:** 7 years; 45 days. (gold docs: sec-data-classification, hr-onboarding-and-exit)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, employee records are retained for a period of 6 years after the employee's last working day. The full and final settlement is processed within 30 days of the employee's last working day. This timeframe allows for the necessary documentation and processing to be completed before the records are archived. Please refer to the HR Policy Manual for more detailed information.
- fact recall: 0.0%; unsupported numbers: ['30']

### u01 (unanswerable) - `answered_unanswerable`
- **Question:** How many days of bereavement leave do employees get?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, eligible employees are entitled to 5 paid bereavement days for the death of a spouse, child, or parent.
- fact recall: n/a; unsupported numbers: ['5']

### u04 (unanswerable) - `answered_unanswerable`
- **Question:** What is the dress code in the office?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** Our company's dress code is business casual. Employees are expected to dress professionally and avoid overly casual or revealing attire. This includes no ripped jeans, flip-flops, or excessive jewelry.
- fact recall: n/a; unsupported numbers: none

### u06 (unanswerable) - `answered_unanswerable`
- **Question:** Is there a referral bonus for recommending a candidate who gets hired?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** Yes, Veridian Systems offers a referral bonus for successful hires. The current policy is as follows: a current employee who refers a qualified candidate who is hired within six months of the referral date will receive a one-time bonus of $1,000. The bonus is paid out after the new hire has completed their 90-day probationary period.
- fact recall: n/a; unsupported numbers: ['1000', '90']

### u07 (unanswerable) - `answered_unanswerable`
- **Question:** What is the mileage reimbursement rate for using my own car for work trips?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** The current mileage reimbursement rate for using your own car for work trips is 58 cents per mile, as per our company's current policy. This rate is subject to change, and any updates will be communicated through our internal channels. Please note that this rate is in effect as of January 2022 and may be adjusted in the future.
- fact recall: n/a; unsupported numbers: ['2022', '58']

### u12 (unanswerable) - `answered_unanswerable`
- **Question:** What is the overtime pay rate for working on weekends?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, overtime pay for weekend work is 1.5 times the regular hourly rate. This applies to all employees, including those in exempt positions. Please refer to the Employee Handbook for the most up-to-date information.
- fact recall: n/a; unsupported numbers: ['1.5']

### u13 (unanswerable) - `answered_unanswerable`
- **Question:** Does the company match employee contributions to the National Pension System?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** Veridian Systems does offer a 401(k) plan, but it does not match employee contributions to the National Pension System. However, we do offer a company-matched 401(k) plan for eligible employees. Please refer to the employee handbook for more details on the plan's specifics.
- fact recall: n/a; unsupported numbers: ['401']

### u15 (unanswerable) - `answered_unanswerable`
- **Question:** What is the largest laptop screen size I can request?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's laptop procurement policy, the largest laptop screen size available for purchase is 17 inches. However, please note that larger screen sizes may not be suitable for all work environments and may require special arrangements. It's recommended to check with IT for specific guidelines on laptop screen size requirements.
- fact recall: n/a; unsupported numbers: ['17']

### u16 (unanswerable) - `answered_unanswerable`
- **Question:** How many days of leave are given for blood donation?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company policy, employees are entitled to 1 paid day off for each blood donation. This is in line with our company's commitment to supporting our employees' charitable endeavors. Please note that this policy may be subject to change, and it's always best to verify with HR for the most up-to-date information.
- fact recall: n/a; unsupported numbers: ['1']

## Vanilla RAG (base paper) - 4 failures

### p04 (paraphrase) - `partial_answer`
- **Question:** I left my work laptop in a taxi. What should I do?
- **Expected:** Report it to IT Security within 1 hour via extension 4357 or security@veridian.example. (gold docs: it-device-policy)
- **Retrieved:** it-device-policy#3, it-device-policy#1, hr-onboarding-and-exit#4, it-device-policy#4
- **Answer:** You should report the incident to IT Security immediately, as per our lost or stolen devices policy. Please call the IT Helpdesk at extension 4357 or email security@veridian.example to report the incident. Additionally, you should also file a police report within 48 hours, as required by our policy. This will help us to initiate the necessary steps to secure your data and recover your device.
- fact recall: 50.0%; unsupported numbers: none

### p10 (paraphrase) - `partial_answer`
- **Question:** I'd like to work from my family's place in Dubai for a few weeks. Is that allowed?
- **Expected:** Up to 30 days per year with prior HR and Legal approval at least 21 days ahead. (gold docs: hr-remote-work)
- **Retrieved:** hr-remote-work#4, hr-parental-leave#4, hr-remote-work#1, fin-travel-policy#1
- **Answer:** Yes, you are allowed to work from your family's place in Dubai for a short period, but it requires prior approval from HR and the Legal team at least 21 days before travel. Please ensure that you book your travel through the corporate TravelDesk portal at least 14 days before departure for international trips. Also, note that you will need to comply with the tax and immigration implications of working from outside India.
- fact recall: 50.0%; unsupported numbers: ['14']

### u05 (unanswerable) - `answered_unanswerable`
- **Question:** How much is the annual performance bonus for a rating of 5?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** hr-performance-review#2, hr-performance-review#3, hr-performance-review#1, hr-performance-review#5
- **Answer:** Unfortunately, the provided context does not explicitly state the annual performance bonus for a rating of 5. However, it does mention that annual salary revisions are communicated in June and are effective from 1 April of the same year, linked to the annual review rating.
- fact recall: n/a; unsupported numbers: ['1']

### u11 (unanswerable) - `answered_unanswerable`
- **Question:** Can I bring my dog to the office?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** hr-code-of-conduct#2, it-device-policy#4, it-password-policy#4, hr-code-of-conduct#3
- **Answer:** No, you cannot bring your dog to the office. Our company's policies do not allow pets in the workplace, with the exception of service animals. This is to maintain a distraction-free and secure work environment. Please consider alternative arrangements for your pet's care while you are at work.
- fact recall: n/a; unsupported numbers: none

## RAG + BM25 - 12 failures

### p01 (paraphrase) - `retrieval_miss`
- **Question:** My kid was just born and I'm the dad. How much time off can I take?
- **Expected:** 15 working days of paid paternity leave within 6 months. (gold docs: hr-parental-leave)
- **Retrieved:** it-mfa-and-access#5, ben-learning-development#4, hr-leave-policy#6, hr-leave-policy#0
- **Answer:** As a new father, you are entitled to take up to 4 hours per month of working time for approved learning activities, but this is not directly related to parental leave. However, the company observes 10 public holidays per year, and you may be eligible for compensatory days off if required to work on a public holiday. According to the Leave Policy, employees receive one compensatory day off, which must be used within 60 days. [hr-leave-policy]
- fact recall: 0.0%; unsupported numbers: ['10', '4', '60']

### p02 (paraphrase) - `generation_error`
- **Question:** I forgot my login credentials. How do I get back into my account?
- **Expected:** Use the self-service portal reset.veridian.internal with MFA, else contact the IT Helpdesk. (gold docs: it-password-policy)
- **Retrieved:** it-password-policy#5, it-password-policy#3, it-password-policy#1, it-password-policy#4
- **Answer:** To regain access to your account, you should contact the Security Operations Centre for assistance. They will investigate repeated lockouts and help you regain access. [it-password-policy] does not specify a direct process for regaining access, but it does mention that repeated lockouts are investigated by the Security Operations Centre. [it-password-policy]
- fact recall: 0.0%; unsupported numbers: none

### p04 (paraphrase) - `generation_error`
- **Question:** I left my work laptop in a taxi. What should I do?
- **Expected:** Report it to IT Security within 1 hour via extension 4357 or security@veridian.example. (gold docs: it-device-policy)
- **Retrieved:** hr-onboarding-and-exit#5, it-device-policy#1, hr-remote-work#1, hr-remote-work#5
- **Answer:** Since the laptop is lost, it should be reported to IT immediately. The employee should contact IT to arrange for a replacement laptop, as the company laptop is managed by IT and is expected to be in good working condition at all times [it-device-policy]. The employee should also provide proof of loss or damage to the laptop to facilitate the replacement process.
- fact recall: 0.0%; unsupported numbers: none

### p06 (paraphrase) - `retrieval_miss`
- **Question:** How much can I spend per head on a dinner with a customer?
- **Expected:** INR 3,000 per person. (gold docs: fin-expense-reimbursement)
- **Retrieved:** hr-onboarding-and-exit#3, sec-data-classification#2, sec-acceptable-ai-use#5, sec-data-classification#4
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### p10 (paraphrase) - `generation_error`
- **Question:** I'd like to work from my family's place in Dubai for a few weeks. Is that allowed?
- **Expected:** Up to 30 days per year with prior HR and Legal approval at least 21 days ahead. (gold docs: hr-remote-work)
- **Retrieved:** hr-remote-work#1, hr-remote-work#5, hr-parental-leave#4, hr-parental-leave#1
- **Answer:** According to the Hybrid and Remote Work Policy, employees are expected to work from their assigned office at least 3 days per week. Working from a family's place in Dubai would not be in compliance with this policy. [hr-remote-work]
- fact recall: 0.0%; unsupported numbers: none

### p11 (paraphrase) - `retrieval_miss`
- **Question:** When will I be eligible to move up to the next level?
- **Expected:** After 18 months in role with ratings of 4+ in two consecutive cycles; promotions effective 1 April. (gold docs: hr-performance-review)
- **Retrieved:** sec-data-classification#1, hr-leave-policy#2, hr-onboarding-and-exit#5, sec-incident-response#3
- **Answer:** You will be eligible to move up to the next level of data classification when the data owner assigns the classification when the information is created. There is no specific timeframe or limit mentioned in the company documents for moving up to the next level of classification. [sec-data-classification]
- fact recall: 0.0%; unsupported numbers: none

### p14 (paraphrase) - `generation_error`
- **Question:** If I quit right after the company pays for my expensive course, do I owe anything?
- **Expected:** For programmes over INR 1,00,000, leaving within 12 months means pro-rata recovery. (gold docs: ben-learning-development)
- **Retrieved:** it-device-policy#4, ben-learning-development#1, fin-procurement#3, it-vpn-remote-access#3
- **Answer:** Since you have used your entire learning budget of INR 40,000 for the course, you do not have any unused budget to roll over to the next financial year. Therefore, you do not owe anything to the company. [ben-learning-development]
- fact recall: 0.0%; unsupported numbers: none

### p15 (paraphrase) - `generation_error`
- **Question:** Can I plug in a pen drive to copy files off my laptop?
- **Expected:** No, USB storage is blocked; exceptions need IT Security approval for up to 30 days. (gold docs: it-device-policy)
- **Retrieved:** it-device-policy#4, it-device-policy#1, hr-leave-policy#6, it-vpn-remote-access#1
- **Answer:** No, you cannot plug in a pen drive to copy files off your company laptop. According to the End-User Device Policy, company files must not be downloaded to personal laptops. [it-device-policy]
- fact recall: 0.0%; unsupported numbers: none

### m02 (multi_doc) - `partial_answer`
- **Question:** When I leave the company, how many leave days are encashed and when is the full and final settlement paid?
- **Expected:** Up to 30 days encashed; F&F within 45 days of last working day. (gold docs: hr-leave-policy, hr-onboarding-and-exit)
- **Retrieved:** hr-leave-policy#1, hr-leave-policy#2, hr-leave-policy#3, it-device-policy#6
- **Answer:** Up to 30 accumulated days of annual leave are encashed at the basic salary rate at the time of exit. The full and final settlement is paid after the employee leaves the company, and unreturned devices are recovered from the full and final settlement at the depreciated value. [hr-leave-policy] [it-device-policy]
- fact recall: 50.0%; unsupported numbers: none

### m04 (multi_doc) - `generation_error`
- **Question:** In my first year on the hybrid model, what is the total home-office support: the one-time stipend plus 12 months of maximum internet reimbursement?
- **Expected:** INR 15,000 + 12 x 1,500 = INR 33,000. (gold docs: hr-remote-work)
- **Retrieved:** hr-remote-work#3, hr-remote-work#1, hr-remote-work#2, hr-remote-work#4
- **Answer:** The one-time home office stipend is INR 15,000. For 12 months of maximum internet reimbursement, the maximum reimbursement per month is INR 1,500, so for 12 months it would be INR 1,500 * 12 = INR 18,000. [hr-remote-work]
- fact recall: 0.0%; unsupported numbers: ['18000']

### m05 (multi_doc) - `partial_answer`
- **Question:** I'm expecting my first baby. How long is my maternity leave and by when must I enrol the baby in health insurance?
- **Expected:** 26 weeks; enrol within 30 days of birth. (gold docs: hr-parental-leave, ben-health-insurance)
- **Retrieved:** hr-parental-leave#1, hr-parental-leave#5, ben-health-insurance#0, ben-health-insurance#1
- **Answer:** You are entitled to 26 weeks of fully paid maternity leave for your first child. You must request your leave in PeopleHub at least 8 weeks before the expected start date of your baby. The group medical insurance policy covers you, your spouse or partner, and up to 2 children, and the policy sum insured is INR 5,00,000 per year. You must enroll your baby in the health insurance policy within the 8-week pre-leave request period, except in emergencies.
- fact recall: 50.0%; unsupported numbers: none

### m06 (multi_doc) - `partial_answer`
- **Question:** I lost a laptop that had customer personal data on it. Who must be informed and within what time limits?
- **Expected:** IT Security within 1 hour; DPO within 6 hours because personal data is involved. (gold docs: it-device-policy, sec-incident-response)
- **Retrieved:** sec-incident-response#5, it-device-policy#3, sec-data-classification#2, it-device-policy#4
- **Answer:** The incident must be escalated to the Data Protection Officer (DPO) within 6 hours of discovery. Additionally, a police report must be filed within 48 hours. The IT Security team must be informed, but the specific time limit is not specified in the provided context.
- fact recall: 66.7%; unsupported numbers: none

## RAG + dense - 3 failures

### f15 (factual) - `generation_error`
- **Question:** How many days in advance must international travel be booked?
- **Expected:** At least 14 days before departure, via TravelDesk. (gold docs: fin-travel-policy)
- **Retrieved:** fin-travel-policy#1, hr-remote-work#4, fin-travel-policy#2, fin-travel-policy#5
- **Answer:** International travel must be booked at least 21 days before departure for approval from HR and the Legal team. [hr-remote-work]
- fact recall: 0.0%; unsupported numbers: ['21']

### m01 (multi_doc) - `partial_answer`
- **Question:** I'm travelling to Mumbai for a client meeting for 3 nights. What is my hotel cap and how long do I have to submit the expense claim?
- **Expected:** INR 7,000 per night; submit within 30 days in SpendWise. (gold docs: fin-travel-policy, fin-expense-reimbursement)
- **Retrieved:** fin-travel-policy#3, fin-expense-reimbursement#5, fin-expense-reimbursement#1, fin-travel-policy#1
- **Answer:** As per the policy, hotel stays in metro cities like Mumbai are capped at INR 7,000 per night. Since you're traveling to Mumbai, your hotel cap is INR 7,000 per night. [fin-travel-policy] [fin-expense-reimbursement]
- fact recall: 50.0%; unsupported numbers: none

### m06 (multi_doc) - `partial_answer`
- **Question:** I lost a laptop that had customer personal data on it. Who must be informed and within what time limits?
- **Expected:** IT Security within 1 hour; DPO within 6 hours because personal data is involved. (gold docs: it-device-policy, sec-incident-response)
- **Retrieved:** it-device-policy#3, it-device-policy#1, sec-incident-response#5, it-device-policy#6
- **Answer:** The IT Security team must be informed, and a police report must also be filed, within 48 hours of the theft. The IT Security team must be contacted within 1 hour of the loss or theft, but the police report must be filed within 48 hours. The IT Security team is responsible for managing company data, and the police report is required to meet regulatory notification obligations. The IT Security team is the team that must be informed.
- fact recall: 33.3%; unsupported numbers: none

## Vaultwise: hybrid RRF + grounded - 2 failures

### p01 (paraphrase) - `retrieval_miss`
- **Question:** My kid was just born and I'm the dad. How much time off can I take?
- **Expected:** 15 working days of paid paternity leave within 6 months. (gold docs: hr-parental-leave)
- **Retrieved:** ben-learning-development#4, hr-leave-policy#6, hr-leave-policy#1, hr-leave-policy#2
- **Answer:** As a new father, you are entitled to 24 days of paid annual leave per calendar year. Annual leave accrues at the rate of 2 days per completed month of service. Since you are a full-time employee, you will accrue leave from the date of your employment. [hr-leave-policy]
- fact recall: 0.0%; unsupported numbers: ['2', '24']

### p14 (paraphrase) - `generation_error`
- **Question:** If I quit right after the company pays for my expensive course, do I owe anything?
- **Expected:** For programmes over INR 1,00,000, leaving within 12 months means pro-rata recovery. (gold docs: ben-learning-development)
- **Retrieved:** hr-onboarding-and-exit#4, hr-onboarding-and-exit#5, ben-learning-development#2, fin-expense-reimbursement#1
- **Answer:** If you pass the certification exam, the company will reimburse the fees for the professional certification exam related to your role. However, if you don't pass the exam, you are only eligible for one retake reimbursement. [ben-learning-development] [fin-expense-reimbursement]
- fact recall: 0.0%; unsupported numbers: none

## LLM only (no retrieval) [llama3.1-8b] - 66 failures

### f01 (factual) - `generation_error`
- **Question:** How many days of paid annual leave do employees get per year?
- **Expected:** 24 days of paid annual leave per calendar year. (gold docs: hr-leave-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's policy, employees are entitled to 20 days of paid annual leave per year, in addition to 8 public holidays. This leave can be taken at a time agreed upon with the manager, subject to business needs. The leave year runs from January 1st to December 31st.
- fact recall: 0.0%; unsupported numbers: ['20', '8']

### f03 (factual) - `generation_error`
- **Question:** When is a medical certificate required for sick leave?
- **Expected:** For sick leave of more than 2 consecutive days. (gold docs: hr-leave-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to Veridian Systems' company policy, a medical certificate is required for sick leave if the absence exceeds three consecutive working days. This is stated in Section 4.2 of the Employee Handbook. The certificate must be provided by a licensed medical practitioner and must include the dates of absence and a diagnosis.
- fact recall: 0.0%; unsupported numbers: none

### f04 (factual) - `generation_error`
- **Question:** How long is maternity leave for the first two children?
- **Expected:** 26 weeks of fully paid leave. (gold docs: hr-parental-leave)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's parental leave policy, new mothers are eligible for 12 weeks of paid maternity leave for their first two children. This leave is in addition to any accrued vacation or sick time. After the 12 weeks, employees may take up to 6 weeks of unpaid parental leave. Please note that this policy is subject to change, and employees should review the most up-to-date policy documents for details.
- fact recall: 0.0%; unsupported numbers: none

### f05 (factual) - `generation_error`
- **Question:** How many days of paternity leave are given?
- **Expected:** 15 working days, within 6 months of birth or adoption. (gold docs: hr-parental-leave)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's parental leave policy, eligible employees are entitled to 10 days of paid paternity leave. This policy applies to all full-time employees who have completed at least 6 months of service. The leave can be taken within the first 6 weeks of the child's birth or adoption. Please note that this policy is subject to change, and you should always check the company's intranet for the most up-to-date information.
- fact recall: 0.0%; unsupported numbers: ['10']

### f06 (factual) - `generation_error`
- **Question:** What is the one-time home office stipend amount?
- **Expected:** INR 15,000. (gold docs: hr-remote-work)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's policy, the one-time home office stipend amount is $500. This stipend is provided to employees who work from home at least 20 hours per week. The stipend is taxable and is paid out annually. Please note that this amount is subject to change, but as of our last update, it remains at $500.
- fact recall: 0.0%; unsupported numbers: ['20', '500']

### f07 (factual) - `generation_error`
- **Question:** How much internet reimbursement can I claim each month?
- **Expected:** Up to INR 1,500 per month. (gold docs: hr-remote-work)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's policy, employees are eligible for a maximum of $50 per month for internet reimbursement. This amount is subject to change, so please check the company's intranet for any updates. Reimbursement is only approved for employees who provide proof of internet usage for work purposes. If you have any questions or need further clarification, please contact your supervisor.
- fact recall: 0.0%; unsupported numbers: ['50']

### f08 (factual) - `generation_error`
- **Question:** What is the maximum value of a gift an employee can accept?
- **Expected:** Gifts must be below INR 5,000. (gold docs: hr-code-of-conduct)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's gift policy, employees are allowed to accept gifts with a value of up to $50. Any gift exceeding this value must be reported to management and may be subject to review. The gift policy is outlined in Section 3, Article 7 of the Veridian Systems Employee Handbook.
- fact recall: 0.0%; unsupported numbers: ['50', '7']

### f09 (factual) - `generation_error`
- **Question:** What is the Ethics Hotline number?
- **Expected:** 1800-200-4455, available 24 hours. (gold docs: hr-code-of-conduct)
- **Retrieved:** (no retrieval)
- **Answer:** The Ethics Hotline number is 1-800-VERIDIAN (1-800-837-3426). This number is available 24/7 for reporting concerns or questions about company ethics and compliance. Calls are confidential and anonymous. The hotline is also available online at veridian.ethicspoint.com.
- fact recall: 0.0%; unsupported numbers: ['1', '7']

### f12 (factual) - `generation_error`
- **Question:** What is the notice period for a manager after confirmation?
- **Expected:** 90 days. (gold docs: hr-onboarding-and-exit)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's policy, a manager's notice period after confirmation is 6 weeks. This is outlined in Section 3, Article 2 of the Veridian Systems Employee Handbook. The notice period applies to all managerial positions, including department heads and team leads. This policy is subject to change, but currently, this is the standard notice period.
- fact recall: 0.0%; unsupported numbers: none

### f14 (factual) - `generation_error`
- **Question:** What is the hotel cap per night in metro cities?
- **Expected:** INR 7,000 per night. (gold docs: fin-travel-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's travel policy, the hotel cap per night in metro cities is $250. This policy applies to all employees traveling for business purposes. The cap is subject to change, but as of the last update, this is the current rate. Please note that this policy may be reviewed and updated periodically.
- fact recall: 0.0%; unsupported numbers: ['250']

### f15 (factual) - `generation_error`
- **Question:** How many days in advance must international travel be booked?
- **Expected:** At least 14 days before departure, via TravelDesk. (gold docs: fin-travel-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to company policy, international travel must be booked at least 30 days in advance to ensure compliance with company travel regulations and to secure the best rates. This policy applies to all employees traveling for business purposes. Failure to book travel in a timely manner may result in additional costs or penalties. Please verify with your manager or the travel department if you have any questions.
- fact recall: 0.0%; unsupported numbers: ['30']

### f16 (factual) - `generation_error`
- **Question:** Within how many days must expenses be submitted in SpendWise?
- **Expected:** Within 30 days of the expense date. (gold docs: fin-expense-reimbursement)
- **Retrieved:** (no retrieval)
- **Answer:** According to company policy, expenses must be submitted in SpendWise within 5 business days of incurring the expense. This allows for timely reimbursement and accurate accounting. Please note that this policy is subject to change, but as of my knowledge cutoff, this is the current requirement.
- fact recall: 0.0%; unsupported numbers: ['5']

### f17 (factual) - `generation_error`
- **Question:** Above what amount is a receipt required for an expense?
- **Expected:** Above INR 500. (gold docs: fin-expense-reimbursement)
- **Retrieved:** (no retrieval)
- **Answer:** According to company policy, a receipt is required for expenses over $50. This is stated in the Employee Expense Policy, Section 3, Subsection B. Please refer to the policy document for more details.
- fact recall: 0.0%; unsupported numbers: ['3', '50']

### f18 (factual) - `generation_error`
- **Question:** What is the cap for client entertainment per person?
- **Expected:** INR 3,000 per person. (gold docs: fin-expense-reimbursement)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's policy, the cap for client entertainment per person is $100. This includes meals, events, and other forms of entertainment. Any expenses above this amount must be approved by a manager in advance. Please refer to the Client Entertainment Policy document for more details.
- fact recall: 0.0%; unsupported numbers: ['100']

### f20 (factual) - `generation_error`
- **Question:** What are the standard vendor payment terms?
- **Expected:** Net 45 days from a valid invoice (30 days for MSMEs). (gold docs: fin-procurement)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's standard payment terms, vendors are paid within 30 days of receiving a valid invoice. This is outlined in our Accounts Payable policy, section 3.2. If a vendor has a different payment arrangement, it must be approved by the Finance department in advance.
- fact recall: 0.0%; unsupported numbers: ['3.2']

### f21 (factual) - `generation_error`
- **Question:** What is the minimum password length?
- **Expected:** 14 characters. (gold docs: it-password-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's password policy, the minimum password length is 12 characters. This is to ensure that passwords are strong and secure. This policy applies to all employees and is enforced by our password management system.
- fact recall: 0.0%; unsupported numbers: ['12']

### f22 (factual) - `partial_answer`
- **Question:** After how many failed sign-in attempts is an account locked, and for how long?
- **Expected:** After 5 consecutive failures, for 15 minutes. (gold docs: it-password-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's security policy, an account is locked after 5 failed sign-in attempts. The lockout duration is 30 minutes, after which the account can be unlocked by the user or an administrator. This policy is in place to prevent unauthorized access to company systems.
- fact recall: 50.0%; unsupported numbers: ['30']

### f23 (factual) - `generation_error`
- **Question:** What is the maximum duration of a just-in-time privileged access request?
- **Expected:** 8 hours per request. (gold docs: it-mfa-and-access)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's policy, the maximum duration of a just-in-time privileged access request is 30 days. This is to ensure that access is only granted for a necessary period and to minimize the risk of unauthorized access. The request must be reviewed and approved by a designated approver before the end of the 30-day period. If the request is not approved, access will be revoked.
- fact recall: 0.0%; unsupported numbers: ['30']

### f24 (factual) - `generation_error`
- **Question:** How often are company laptops refreshed?
- **Expected:** Every 4 years. (gold docs: it-device-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's IT policy, company laptops are refreshed every 3 years. This is to ensure that employees have access to the latest technology and security features. The refresh cycle is managed by the IT department, who will notify employees when their laptop is due for replacement.
- fact recall: 0.0%; unsupported numbers: ['3']

### f25 (factual) - `generation_error`
- **Question:** After how many hours does a VPN session disconnect automatically?
- **Expected:** After 12 hours (or 30 minutes of inactivity). (gold docs: it-vpn-remote-access)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's VPN policy, a VPN session will automatically disconnect after 8 hours of inactivity. This is to prevent unauthorized access and ensure security. If you need to stay connected for an extended period, you can manually reconnect.
- fact recall: 0.0%; unsupported numbers: ['8']

### f27 (factual) - `generation_error`
- **Question:** Within how many hours must a personal data breach be escalated to the DPO?
- **Expected:** Within 6 hours of discovery. (gold docs: sec-incident-response)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's Data Protection Policy, a personal data breach must be escalated to the Data Protection Officer (DPO) within 2 hours of discovery. This allows for prompt action to be taken to mitigate the breach and minimize potential harm to individuals. The DPO will then coordinate with relevant teams to investigate and respond to the breach.
- fact recall: 0.0%; unsupported numbers: ['2']

### f29 (factual) - `generation_error`
- **Question:** What is the family floater sum insured for group medical insurance?
- **Expected:** INR 5,00,000 per year. (gold docs: ben-health-insurance)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's group medical insurance policy, the family floater sum insured is $100,000. This amount covers all eligible family members under a single policy. The policy also includes a deductible of $500 per person per year. Please note that this information is subject to change, and you can verify it with HR or the insurance provider if needed.
- fact recall: 0.0%; unsupported numbers: ['100000', '500']

### f30 (factual) - `generation_error`
- **Question:** What is the annual learning budget per employee?
- **Expected:** INR 40,000 per financial year. (gold docs: ben-learning-development)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's Learning and Development Policy, each employee is allocated an annual learning budget of $1,500 to support their professional growth and development. This budget can be used for approved courses, training programs, and certifications. The budget is reviewed and updated annually, and employees can submit requests for budget allocation through our internal learning portal.
- fact recall: 0.0%; unsupported numbers: ['1500']

### p01 (paraphrase) - `generation_error`
- **Question:** My kid was just born and I'm the dad. How much time off can I take?
- **Expected:** 15 working days of paid paternity leave within 6 months. (gold docs: hr-parental-leave)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's parental leave policy, new parents are eligible for up to 12 weeks of paid parental leave. This leave can be taken within the first year of the child's birth or adoption. You'll need to submit a request to your manager and HR for approval. Please review the policy document for more details and requirements.
- fact recall: 0.0%; unsupported numbers: none

### p02 (paraphrase) - `generation_error`
- **Question:** I forgot my login credentials. How do I get back into my account?
- **Expected:** Use the self-service portal reset.veridian.internal with MFA, else contact the IT Helpdesk. (gold docs: it-password-policy)
- **Retrieved:** (no retrieval)
- **Answer:** To reset your login credentials, please visit the Veridian Systems Intranet and click on the "Forgot Password" link on the login page. Follow the prompts to answer your security questions and reset your password. If you're still having trouble, contact the IT department for assistance. They can also help you reset your login credentials if needed.
- fact recall: 0.0%; unsupported numbers: none

### p03 (paraphrase) - `partial_answer`
- **Question:** Can I take an evening job at another company on the side?
- **Expected:** Only with prior written approval from HR, and it must be disclosed as a potential conflict of interest. (gold docs: hr-code-of-conduct)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's policy, employees are allowed to work part-time or freelance jobs outside of Veridian Systems, as long as they do not conflict with their primary responsibilities or compromise company confidentiality. However, prior approval from your supervisor is required before taking on any outside work. Please review Section 3, Subsection B of the Employee Handbook for more details.
- fact recall: 50.0%; unsupported numbers: none

### p04 (paraphrase) - `generation_error`
- **Question:** I left my work laptop in a taxi. What should I do?
- **Expected:** Report it to IT Security within 1 hour via extension 4357 or security@veridian.example. (gold docs: it-device-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's asset management policy, if a company device is lost or stolen, you must report it to the IT department immediately. You can contact us at [IT email] or [IT phone number] to initiate the reporting process. We will then guide you through the necessary steps to secure the device and prevent any potential data breaches. Please also file a police report if the taxi is located.
- fact recall: 0.0%; unsupported numbers: none

### p05 (paraphrase) - `generation_error`
- **Question:** Someone emailed me asking me to verify my bank details through a link. What do I do?
- **Expected:** Do not click; report it with the Report Phish button. (gold docs: sec-incident-response)
- **Retrieved:** (no retrieval)
- **Answer:** Do not click on the link or provide any personal information. Veridian Systems will never ask you to verify bank details through an email link. If you're unsure, contact the IT department or your supervisor for guidance.
- fact recall: 0.0%; unsupported numbers: none

### p06 (paraphrase) - `generation_error`
- **Question:** How much can I spend per head on a dinner with a customer?
- **Expected:** INR 3,000 per person. (gold docs: fin-expense-reimbursement)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's expense policy, meals with customers are subject to a $50 per person limit. This includes tax and tip. Any expenses exceeding this amount must be approved by a manager in advance. Please refer to the Employee Handbook, Section 3, for more details.
- fact recall: 0.0%; unsupported numbers: ['3', '50']

### p07 (paraphrase) - `generation_error`
- **Question:** How long until I get my money back once my claim is approved?
- **Expected:** Within 10 business days of final approval. (gold docs: fin-expense-reimbursement)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's Employee Benefits Policy, approved claims are typically reimbursed within 2-3 business days. The reimbursement will be processed through direct deposit into your bank account. If you have any issues with your reimbursement, please contact our HR department.
- fact recall: 0.0%; unsupported numbers: ['2']

### p09 (paraphrase) - `generation_error`
- **Question:** Do I have to come into the office every day?
- **Expected:** No, at least 3 days per week (Tue-Thu core days). (gold docs: hr-remote-work)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's Flexible Work Arrangement policy, employees are expected to be available and responsive during core hours (10am-4pm) but are not required to physically be in the office every day. However, it is recommended that employees spend at least one day per week in the office for team collaboration and meetings. Remote work arrangements can be discussed with your manager on a case-by-case basis. Please refer to the Flexible Work Arrangement policy document for more details.
- fact recall: 0.0%; unsupported numbers: none

### p10 (paraphrase) - `generation_error`
- **Question:** I'd like to work from my family's place in Dubai for a few weeks. Is that allowed?
- **Expected:** Up to 30 days per year with prior HR and Legal approval at least 21 days ahead. (gold docs: hr-remote-work)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's Remote Work Policy, employees are allowed to work from a remote location outside of the country with prior approval from their manager and HR. However, please note that Dubai is considered a high-risk location due to data protection and security concerns. You will need to submit a Remote Work Request Form and obtain approval from your manager and HR before making any arrangements.
- fact recall: 0.0%; unsupported numbers: none

### p11 (paraphrase) - `generation_error`
- **Question:** When will I be eligible to move up to the next level?
- **Expected:** After 18 months in role with ratings of 4+ in two consecutive cycles; promotions effective 1 April. (gold docs: hr-performance-review)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's performance review policy, employees are eligible to move up to the next level after completing 12 months of service and meeting the required performance targets. These targets are outlined in the Performance Review Guidelines document, which can be found on the company intranet. Your supervisor will also provide you with a personalized review of your progress. Please check with your supervisor for more information on your specific situation.
- fact recall: 0.0%; unsupported numbers: ['12']

### p12 (paraphrase) - `generation_error`
- **Question:** How much does the company give me towards a gym membership?
- **Expected:** Wellness allowance of INR 12,000 per year. (gold docs: ben-health-insurance)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's benefits package, Veridian Systems offers a $50 monthly reimbursement for gym memberships. This reimbursement is available to all full-time employees. You can submit your gym membership expenses through our online benefits portal.
- fact recall: 0.0%; unsupported numbers: ['50']

### p13 (paraphrase) - `generation_error`
- **Question:** Can my mom and dad be included in my medical cover?
- **Expected:** Yes, via an optional employee-paid top-up of INR 3,00,000. (gold docs: ben-health-insurance)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's medical benefits policy, family members are eligible for coverage, but only spouses and dependent children are included. Parents are not eligible for coverage under our standard medical plan. However, you may want to review our Flexible Spending Account (FSA) policy, which allows for reimbursement of certain family-related medical expenses.
- fact recall: 0.0%; unsupported numbers: none

### p14 (paraphrase) - `generation_error`
- **Question:** If I quit right after the company pays for my expensive course, do I owe anything?
- **Expected:** For programmes over INR 1,00,000, leaving within 12 months means pro-rata recovery. (gold docs: ben-learning-development)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's policy, if you resign within 6 months of completing a company-sponsored course, you are required to repay the full cost of the course. This policy is outlined in Section 3, Article 7 of our Employee Handbook. If you resign after 6 months, you are not required to repay the cost. Please review the handbook for more details.
- fact recall: 0.0%; unsupported numbers: ['3', '6', '7']

### p15 (paraphrase) - `generation_error`
- **Question:** Can I plug in a pen drive to copy files off my laptop?
- **Expected:** No, USB storage is blocked; exceptions need IT Security approval for up to 30 days. (gold docs: it-device-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's Data Security Policy, employees are allowed to use personal devices to transfer files, but they must be encrypted and approved by IT in advance. Please submit a request to IT to obtain approval for your pen drive. Once approved, you can plug it in to transfer files.
- fact recall: 0.0%; unsupported numbers: none

### p16 (paraphrase) - `partial_answer`
- **Question:** What should I do if my remote connection to office systems keeps failing?
- **Expected:** Check internet, restart SecureLink, switch gateway, then ServiceHub or ext 4357. (gold docs: it-vpn-remote-access)
- **Retrieved:** (no retrieval)
- **Answer:** If your remote connection to office systems keeps failing, please try restarting your VPN connection and ensure your internet connection is stable. If the issue persists, contact our IT department for assistance. They can help troubleshoot the issue and provide a resolution. You can reach them at [IT department contact information].
- fact recall: 50.0%; unsupported numbers: none

### p18 (paraphrase) - `generation_error`
- **Question:** Can I read work email on my own phone?
- **Expected:** Yes, after enrolling in the company MDM app. (gold docs: it-device-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to Veridian Systems' Email Policy (Section 3, Article 2), employees are allowed to access their work email on personal devices, but only for work-related purposes. Personal use of company email is not permitted. You can find the full policy on the company intranet under "Employee Resources".
- fact recall: 0.0%; unsupported numbers: ['2', '3']

### p19 (paraphrase) - `generation_error`
- **Question:** I got a new phone. How do I set up my second login factor again?
- **Expected:** Raise an IT Helpdesk ticket; identity is verified on a video call with your manager. (gold docs: it-mfa-and-access)
- **Retrieved:** (no retrieval)
- **Answer:** To set up your second login factor, go to the Veridian Systems Intranet and click on "My Account" > "Security Settings". From there, follow the prompts to add a new authentication method, such as a fingerprint reader or a security token. You can also refer to the "Security Best Practices" document in the company's knowledge base for more detailed instructions. If you have any issues, feel free to reach out to the IT department for assistance.
- fact recall: 0.0%; unsupported numbers: none

### p20 (paraphrase) - `generation_error`
- **Question:** Am I allowed to fly business class to the US?
- **Expected:** Only Directors and above, for flights over 6 hours; others fly premium economy. (gold docs: fin-travel-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company travel policy, employees are allowed to upgrade to business class on international flights, including those to the US, if it is deemed necessary for business purposes or if the employee has accumulated sufficient travel points. However, the employee must obtain approval from their manager in advance. The upgrade must also be booked through our designated travel agency.
- fact recall: 0.0%; unsupported numbers: none

### m01 (multi_doc) - `generation_error`
- **Question:** I'm travelling to Mumbai for a client meeting for 3 nights. What is my hotel cap and how long do I have to submit the expense claim?
- **Expected:** INR 7,000 per night; submit within 30 days in SpendWise. (gold docs: fin-travel-policy, fin-expense-reimbursement)
- **Retrieved:** (no retrieval)
- **Answer:** According to company policy, the hotel cap for international travel is $250 per night. You should submit your expense claim within 5 business days of returning to the office. Please note that you'll need to provide a receipt and a detailed breakdown of your expenses.
- fact recall: 0.0%; unsupported numbers: ['250', '5']

### m02 (multi_doc) - `partial_answer`
- **Question:** When I leave the company, how many leave days are encashed and when is the full and final settlement paid?
- **Expected:** Up to 30 days encashed; F&F within 45 days of last working day. (gold docs: hr-leave-policy, hr-onboarding-and-exit)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's policy, employees are entitled to encash 30 days of leave balance upon resignation. The full and final settlement, including encashment of leave, is paid on the last working day of the month following the employee's last day of work. This is as per Section 3.2 of the Employee Handbook.
- fact recall: 50.0%; unsupported numbers: ['3.2']

### m04 (multi_doc) - `generation_error`
- **Question:** In my first year on the hybrid model, what is the total home-office support: the one-time stipend plus 12 months of maximum internet reimbursement?
- **Expected:** INR 15,000 + 12 x 1,500 = INR 33,000. (gold docs: hr-remote-work)
- **Retrieved:** (no retrieval)
- **Answer:** According to company policy, the one-time stipend for home-office setup is $500. Additionally, the company reimburses up to $100 per month for internet costs for 12 months, totaling $1,200. This support is provided to all employees on the hybrid model in their first year.
- fact recall: 0.0%; unsupported numbers: ['100', '1200', '500']

### m05 (multi_doc) - `partial_answer`
- **Question:** I'm expecting my first baby. How long is my maternity leave and by when must I enrol the baby in health insurance?
- **Expected:** 26 weeks; enrol within 30 days of birth. (gold docs: hr-parental-leave, ben-health-insurance)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's Family Leave Policy, eligible employees are entitled to 12 weeks of unpaid maternity leave. You must provide at least 30 days' written notice to HR before taking leave. As for health insurance, you must enroll your baby within 30 days of birth to ensure coverage. Please review the Family Leave Policy document for more details.
- fact recall: 50.0%; unsupported numbers: none

### m06 (multi_doc) - `partial_answer`
- **Question:** I lost a laptop that had customer personal data on it. Who must be informed and within what time limits?
- **Expected:** IT Security within 1 hour; DPO within 6 hours because personal data is involved. (gold docs: it-device-policy, sec-incident-response)
- **Retrieved:** (no retrieval)
- **Answer:** According to Veridian Systems' Data Breach Policy, you must immediately notify the IT department and the Data Protection Officer (DPO) in writing. The DPO will then inform the relevant regulatory bodies and customers affected by the breach, as per the policy's notification procedures. This notification must be made within 24 hours of discovering the breach. The IT department will also assist in containing and investigating the incident.
- fact recall: 33.3%; unsupported numbers: ['24']

### m07 (multi_doc) - `partial_answer`
- **Question:** On my last working day, what happens to my system access and my laptop?
- **Expected:** Access is revoked by 6:00 PM; the laptop must be returned to IT. (gold docs: hr-onboarding-and-exit, it-mfa-and-access, it-device-policy)
- **Retrieved:** (no retrieval)
- **Answer:** According to company policy, your system access will be revoked on your last working day, and you will be required to return your company laptop to the IT department. This is to ensure the security and integrity of our systems and data. You will also be asked to complete a handover of any outstanding tasks and projects. Please confirm your last working day with your manager to ensure a smooth transition.
- fact recall: 50.0%; unsupported numbers: none

### m08 (multi_doc) - `partial_answer`
- **Question:** I'm a new joiner still on probation. How many days of annual leave can I use and what is my notice period?
- **Expected:** At most 6 days of annual leave; 15 days notice. (gold docs: hr-leave-policy, hr-onboarding-and-exit)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's Employee Handbook, as a new joiner on probation, you are entitled to 5 days of annual leave, which can be taken after completing 3 months of service. Your notice period is 1 week for the first 6 months of employment. After 6 months, your notice period will be 2 weeks. Please review the Employee Handbook for more details.
- fact recall: 50.0%; unsupported numbers: ['5']

### m09 (multi_doc) - `generation_error`
- **Question:** I want to spend INR 60,000 on a certification course. Who must approve the learning request, and who must approve the expense claim?
- **Expected:** Manager + HR Business Partner for the request; manager + Finance Controller for a claim above INR 50,000. (gold docs: ben-learning-development, fin-expense-reimbursement)
- **Retrieved:** (no retrieval)
- **Answer:** According to Veridian Systems' Learning and Development Policy, a Manager's approval is required for learning requests exceeding INR 30,000. For expense claims, the Finance Team must approve all requests exceeding INR 20,000. Your Manager will need to approve the learning request, and then you can submit the expense claim to the Finance Team for approval.
- fact recall: 0.0%; unsupported numbers: ['20000', '30000']

### m10 (multi_doc) - `partial_answer`
- **Question:** How long are employee records retained after exit, and within how many days of the last working day is the full and final settlement processed?
- **Expected:** 7 years; 45 days. (gold docs: sec-data-classification, hr-onboarding-and-exit)
- **Retrieved:** (no retrieval)
- **Answer:** According to company policy, employee records are retained for 7 years after exit. The full and final settlement is processed within 30 days of the last working day. This ensures compliance with relevant employment laws and regulations. Please refer to the HR Policy Manual for further details.
- fact recall: 50.0%; unsupported numbers: ['30']

### u01 (unanswerable) - `answered_unanswerable`
- **Question:** How many days of bereavement leave do employees get?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's policy, employees are entitled to 3 days of bereavement leave for immediate family members and 1 day for extended family members. This leave is unpaid, but can be taken in addition to accrued vacation time. The policy also allows for flexible scheduling to accommodate funeral arrangements. Please refer to the Employee Handbook for more details.
- fact recall: n/a; unsupported numbers: ['1', '3']

### u02 (unanswerable) - `answered_unanswerable`
- **Question:** What is the vesting schedule for employee stock options?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's equity compensation policy, employee stock options vest at a rate of 25% per year over a 4-year period, with a 1-year cliff. This means that 25% of the options will vest after 1 year, and the remaining 75% will vest in equal installments over the next 3 years. The policy also states that options expire 10 years from the date of grant.
- fact recall: n/a; unsupported numbers: ['1', '10', '25', '3', '4', '75']

### u03 (unanswerable) - `answered_unanswerable`
- **Question:** Does the company run a shuttle bus from the metro station to the office?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's transportation policy, Veridian Systems offers a complimentary shuttle bus service from the downtown metro station to our office. The shuttle runs on weekdays, Monday through Friday, and the schedule is posted on the company's intranet. The bus stop is located near the metro station's main entrance. Please check the intranet for the most up-to-date schedule and any service alerts.
- fact recall: n/a; unsupported numbers: none

### u04 (unanswerable) - `answered_unanswerable`
- **Question:** What is the dress code in the office?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's dress code policy, business casual attire is required for all employees. This includes dress pants or skirts, button-down shirts, and blouses. Jeans and t-shirts are allowed on Fridays, but must be in good condition and not overly casual. Any questions or concerns should be directed to HR.
- fact recall: n/a; unsupported numbers: none

### u05 (unanswerable) - `answered_unanswerable`
- **Question:** How much is the annual performance bonus for a rating of 5?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's compensation policy, an employee with a rating of 5 is eligible for a bonus of 15% of their annual salary. This bonus is paid out in two installments, one in June and one in December. The bonus amount is calculated based on the employee's current salary, not their salary at the time of the previous bonus payment. Please note that this policy is subject to change, and any updates will be communicated through company-wide announcements.
- fact recall: n/a; unsupported numbers: ['15']

### u06 (unanswerable) - `answered_unanswerable`
- **Question:** Is there a referral bonus for recommending a candidate who gets hired?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's Employee Referral Program policy, yes, there is a referral bonus for recommending a candidate who gets hired. The bonus amount is $1,000 for external referrals and $500 for internal referrals. The bonus is paid out after the new hire has completed their 90-day probationary period.
- fact recall: n/a; unsupported numbers: ['1000', '500', '90']

### u07 (unanswerable) - `answered_unanswerable`
- **Question:** What is the mileage reimbursement rate for using my own car for work trips?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's travel policy, the mileage reimbursement rate is 58.5 cents per mile for business use of a personal vehicle. This rate is subject to change, so please check the company's intranet for any updates. You can also refer to the Veridian Systems Travel Policy document for more information.
- fact recall: n/a; unsupported numbers: ['58.5']

### u08 (unanswerable) - `answered_unanswerable`
- **Question:** How many months of sabbatical can I take after 5 years of service?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's policy, after 5 years of service, employees are eligible for 6 months of sabbatical leave. This can be taken in one block or split into two periods, with prior approval from HR. The sabbatical leave is intended to provide a break from work and can be used for personal or professional development. Please review the Sabbatical Leave Policy document for more details.
- fact recall: n/a; unsupported numbers: ['6']

### u09 (unanswerable) - `answered_unanswerable`
- **Question:** What is the password for the guest Wi-Fi network?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** The password for the guest Wi-Fi network is "VeridianGuest". This password is publicly available on the company's website and is also displayed on the guest Wi-Fi login page. It is changed periodically, but the current password is valid for the next 30 days.
- fact recall: n/a; unsupported numbers: ['30']

### u10 (unanswerable) - `answered_unanswerable`
- **Question:** Who is the current CEO of Veridian Systems?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** The current CEO of Veridian Systems is Emily J. Miller. She has been in this position since January 2022. According to the company's leadership page, she is responsible for setting the overall direction and strategy for the company.
- fact recall: n/a; unsupported numbers: ['2022']

### u11 (unanswerable) - `answered_unanswerable`
- **Question:** Can I bring my dog to the office?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to Veridian Systems' Employee Handbook, Section 3, Article 7, pets are not allowed in the office, with the exception of service animals. If you have a service animal, please provide documentation to HR. Regular pets are not permitted due to allergies and space constraints.
- fact recall: n/a; unsupported numbers: ['3', '7']

### u12 (unanswerable) - `answered_unanswerable`
- **Question:** What is the overtime pay rate for working on weekends?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's Time-Off and Overtime Policy (Section 3, Article 2), employees are entitled to 1.5 times their regular hourly rate for working on weekends. This rate applies to all non-exempt employees who work on Saturdays or Sundays. The policy also states that employees must receive prior approval from their supervisor before working overtime on weekends.
- fact recall: n/a; unsupported numbers: ['1.5', '2', '3']

### u13 (unanswerable) - `answered_unanswerable`
- **Question:** Does the company match employee contributions to the National Pension System?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's benefits policy, Veridian Systems matches 50% of employee contributions to the National Pension System. This is a standard benefit for all eligible employees. The matching rate is subject to change, but as of the last update, this is the current policy.
- fact recall: n/a; unsupported numbers: ['50']

### u14 (unanswerable) - `answered_unanswerable`
- **Question:** How much is the relocation allowance when moving to a different city for work?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's relocation policy, the allowance for moving to a different city for work is $10,000. This amount is provided to help offset the costs of relocation, including housing, transportation, and other expenses. The allowance is taxable and is paid out in a lump sum upon completion of the move. Please note that this policy is subject to change, and you should verify the details with HR for the most up-to-date information.
- fact recall: n/a; unsupported numbers: ['10000']

### u15 (unanswerable) - `answered_unanswerable`
- **Question:** What is the largest laptop screen size I can request?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's travel and expense policy, the maximum laptop screen size that can be reimbursed is 15.6 inches. This is to ensure that employees can easily transport and store their laptops. If you need a larger screen size, you may need to discuss it with your manager or IT department.
- fact recall: n/a; unsupported numbers: ['15.6']

### u16 (unanswerable) - `answered_unanswerable`
- **Question:** How many days of leave are given for blood donation?
- **Expected:** Not covered. (gold docs: none)
- **Retrieved:** (no retrieval)
- **Answer:** According to our company's policy, employees who donate blood are eligible for one day of paid leave. This is in addition to any other leave they may have accrued. The leave is granted to allow for recovery time and to encourage employees to participate in blood donation programs. Please note that this policy may be subject to change, so it's always a good idea to check with HR for the most up-to-date information.
- fact recall: n/a; unsupported numbers: none

## Vaultwise: hybrid RRF + grounded [llama3.1-8b] - 3 failures

### p01 (paraphrase) - `retrieval_miss`
- **Question:** My kid was just born and I'm the dad. How much time off can I take?
- **Expected:** 15 working days of paid paternity leave within 6 months. (gold docs: hr-parental-leave)
- **Retrieved:** ben-learning-development#4, hr-leave-policy#6, hr-leave-policy#1, hr-leave-policy#2
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### p11 (paraphrase) - `false_refusal`
- **Question:** When will I be eligible to move up to the next level?
- **Expected:** After 18 months in role with ratings of 4+ in two consecutive cycles; promotions effective 1 April. (gold docs: hr-performance-review)
- **Retrieved:** hr-performance-review#3, hr-leave-policy#2, hr-onboarding-and-exit#5, sec-data-classification#1
- **Answer:** I don't have enough information in the company documents to answer that.
- fact recall: 0.0%; unsupported numbers: none

### p14 (paraphrase) - `generation_error`
- **Question:** If I quit right after the company pays for my expensive course, do I owe anything?
- **Expected:** For programmes over INR 1,00,000, leaving within 12 months means pro-rata recovery. (gold docs: ben-learning-development)
- **Retrieved:** hr-onboarding-and-exit#4, hr-onboarding-and-exit#5, ben-learning-development#2, fin-expense-reimbursement#1
- **Answer:** You are eligible for reimbursement of the course fees if you pass the exam, and one retake is reimbursed if the first attempt is unsuccessful [ben-learning-development]. The company reimburses professional certification exam fees after the employee passes the exam [ben-learning-development]. If you submit your resignation and leave the company, you must return company assets, including laptops and access badges, on your last working day [hr-onboarding-and-exit]. The full and final settlement is processed within 45 days of your last working day, and you would not owe anything related to the course fees at that time [hr-onboarding-and-exit].
- fact recall: 0.0%; unsupported numbers: ['45']
