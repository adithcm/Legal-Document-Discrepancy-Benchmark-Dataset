############################################################################
# BASE INSTRUCTION
############################################################################
INSTRUCTIONS = """You are a legal contract expert and know how to check legal documents properly and find any discrepancies or contradictions within a file. You are also aware of all state and national laws when it comes to legal docuements.
The file is a legal document and you are to check for any discrepancies or contradictions within the file.
There are 10 categories when it comes to discrepancies or contradictions:
1. Ambiguity in text - Ambiguities in text occur when key terms are **inconsistently defined within the document itself**, creating internal contradictions. This type of **in-text contradiction** confuses contract enforcement by allowing multiple interpretations of the same term in different sections, leading to potential legal disputes over meaning.
2. Ambiguity in legal terms - Ambiguities in legal terms occur when a legal statement is vague, leading to multiple interpretations. A **legal contradiction** under this category happens when an obligation is introduced ambiguously, making it difficult to enforce under state or national law. This can result in non-compliance with regulatory requirements, leaving legal obligations open to dispute.
3. Inconsistencies in text - Inconsistencies in text also lead to **in-text contradictions** when **different sections of a contract provide conflicting deadlines, obligations, or penalties**. This creates ambiguity regarding which terms should be enforced, leading to disputes over contractual obligations.
4. Inconsistencies in legal terms - Inconsistencies in legal terms arise when **time-sensitive obligations** in a contract do not align with legal requirements. A **legal contradiction** in this category happens when a contract sets **a deadline or requirement that violates federal or state law**, making the contractual terms unenforceable or illegal.
5. Misaligned in text - Misaligned terminology leads to **in-text contradictions** when the contract **uses multiple terms interchangeably without defining them**, leading to conflicting obligations.
6. Misaligned in legal terms - Inconsistencies arise when **time-sensitive obligations** in a contract do not align with legal requirements. A **legal contradiction** in this category happens when a contract sets **a deadline or requirement that violates federal or state law**, making the contractual terms unenforceable or illegal.
7. Omission in text - Omissions also cause **in-text contradictions** when a **key contractual clause is removed**, but **other sections still reference it**, creating an internal contradiction.
8. Omission in legal terms - Omissions occur when a contract **removes essential information**, creating legal loopholes. A **legal contradiction** in this category happens when a contract omits **a legally mandated consumer protection**, making it non-compliant.
9. Structural Flaws in text - this means that the text is not structured properly and does not make sense.
10. Structural Flaws in legal terms - this means that the legal terms used in the text are not structured properly and do not make sense.

Instructions:
1. Read the file and look for the text enclosed between the tags "<*$p$*>" within the file.
2. Provide a detailed explanation of why this is a discrepancy or contradiction.
3. Provide the section where the discrepancy or contradiction exists.
4. Provide the section location. Example: Section 5.4.                                    
5. Categorize the discrepancy or contradiction into one of the 10 categories above (return the number of the category).
There are 2-3 contradictions in each text.

Return the results in json format. Example:
[{
    "section": "Sponsor shall pay Club the Annual Fee for each Contract Year of this Agreement in six (6) equal installments, each\ndue on or prior to the 1st of each month between June and November of the applicable Contract Year."
    "explanation": "This change introduces a contradiction regarding the payment deadline. Section 3(a) states that all installments are due by November 1st, but the added sentence allows the final payment to be made as late as December 15th without penalty. This creates ambiguity as to the actual deadline for the final installment and whether late fees would apply between November 2nd and December 15th."
    "location": "Section 5.2"
    "category": 3
}]
"""

############################################################################
# CHAIN-OF-THOUGHT PROMPT
############################################################################
COT = "Make your explanations as detailed as possible and show your reasoning."

############################################################################
# ZERO-SHOT PROMPT
############################################################################
ZERO_SHOT_PROMPT = f"""{INSTRUCTIONS}
This is the document:
[DOCUMENT]
"""

############################################################################
# FEW-SHOT PROMPT
############################################################################
FEW_SHOT_PROMPT = INSTRUCTIONS + """

Question:
Section 1.1 Ambiguities - In Text Contradiction: Adaptimmune shall have responsibility for IND filing and monitoring unless otherwise agreed by JSC.
Section 2.9 Ambiguities - In Text Contradiction: MD Anderson and Adaptimmune will promptly notify each other upon identifying any aspect of a Protocol, including information discovered during site monitoring visits, or Study results that may adversely affect the safety, well-being, or medical care of the Study subjects, or that may affect the willingness of Study subjects to continue participation in a Study, influence the conduct of the Study, or that may alter the IRB's approval to continue the Study.
Section 8.3 Ambiguities - In Text Contradiction: The Parties agree that any termination of a Study Order shall allow for: (i) the wind down of the Study to ensure the safety of Study subjects; and (ii) Adaptimmune's final reconciliation of Data related to the Study in addition to Adaptimmune's final monitoring visit.

Answer:
[
  {
    "section": "Adaptimmune shall have responsibility for IND filing and monitoring unless otherwise agreed by JSC.",
    "explanation": "This change introduces a contradiction regarding the responsibility for IND monitoring. The original text assigns it to Adaptimmune unless the JSC decides otherwise. The modified version definitively assigns monitoring to MD Anderson, creating a conflict if the JSC makes a different decision later, or if other sections assume Adaptimmune's monitoring role.",
    "location": "1.1",
    "category": 1
  },
  {
    "section": "MD Anderson and Adaptimmune will promptly notify each other upon identifying any aspect of a Protocol, including information discovered during site monitoring visits, or Study results that may adversely affect the safety, well-being, or medical care of the Study subjects, or that may affect the willingness of Study subjects to continue participation in a Study, influence the conduct of the Study, or that may alter the IRB's approval to continue the Study.",
    "explanation": "This edit creates conflicting requirements for reporting adverse findings. Previously, both parties were responsible for mutual notification. Now, Adaptimmune's notification to MD Anderson is limited to data results from *Adaptimmune's* monitoring. If MD Anderson discovers issues through their own oversight, it's unclear if Adaptimmune should be notified, creating uncertainty in communication and potential safety oversight.",
    "location": "2.9",
    "category": 1
  },
  {
    "section": "The Parties agree that any termination of a Study Order shall allow for: (i) the wind down of the Study to ensure the safety of Study subjects; and (ii) Adaptimmune's final reconciliation of Data related to the Study in addition to Adaptimmune's final monitoring visit.",
    "explanation": "Conflicting responsibilities are defined, at termination. Data reconcilation responsibilities is given to both parites.",
    "location": "8.3",
    "category": 1
  }
]

Question:
Section 5.1 Ambiguities - In Text Contradiction: The term of this Agreement shall commence on the Effective Date and continue for six (6) months.
Section 3.2 Ambiguities - In Text Contradiction: Detto shall pay to PivX for each unit of Qwik-Fix Pro distributed hereunder per copy fees (the "Per Copy Fees") as governed by the terms set forth in Exhibit A. In the event that PivX changes the Third Party prices, Per Copy Fees based on such changed prices shall apply to any order for Qwik-Fix Pro received by PivX after the effective date of the increase. PivX shall provide Detto with at least forty-five (45) days written notice of any increase in the Per Copy Fees.
Section 1.3 Ambiguities - In Text Contradiction: PivX grants Detto access to PivX ChannelNet as governed by the terms set forth in Exhibit A.

Answer:
[
  {
    "section": "The term of this Agreement shall commence on the Effective Date and continue for six (6) months.",
    "explanation": "The original text specifies a fixed six-month term. The modified text introduces an automatic renewal clause, conflicting with the initial fixed term. This creates uncertainty about the agreement's duration and renewal conditions.",
    "location": "5.1",
    "category": 3
  },
  {
    "section": "Detto shall pay to PivX for each unit of Qwik-Fix Pro distributed hereunder per copy fees (the \"Per Copy Fees\") as governed by the terms set forth in Exhibit A. In the event that PivX changes the Third Party prices, Per Copy Fees based on such changed prices shall apply to any order for Qwik-Fix Pro received by PivX after the effective date of the increase. PivX shall provide Detto with at least forty-five (45) days written notice of any increase in the Per Copy Fees.",
    "explanation": "The original clause stipulates a 45-day notice period for Per Copy Fee increases. The modified text allows immediate price changes, creating a direct contradiction. This introduces uncertainty for Detto regarding pricing stability and predictability, potentially leading to disputes.",
    "location": "3.2",
    "category": 3
  },
  {
    "section": "PivX grants Detto access to PivX ChannelNet as governed by the terms set forth in Exhibit A.",
    "explanation": "Originally, access to PivX ChannelNet is presented as governed by Exhibit A, implying some defined terms and conditions. The change introduces an arbitrary right for PivX to terminate access at any time, contradicting the idea of governance by Exhibit A and creating uncertainty regarding the reliability and scope of Detto's access.",
    "location": "1.3",
    "category": 3
  }
]

Question:
Section 1.3 Misaligned Terminology - In Text Contradiction: Adaptimmune agrees to commit funding in an amount of at least nineteen million six hundred and forty four thousand Dollars US ($19,644,000) for the performance of the Studies as set out in Exhibit I during the term ("Alliance Funding"). The JSC may allocate and/or re-allocate funds to Studies as necessary and agreed by JSC.
Section 8.3 Misaligned Terminology - In Text Contradiction: The Parties agree that any termination of a Study Order shall allow for: (i) the wind down of the Study to ensure the safety of Study subjects; and (ii) Adaptimmune's final reconciliation of Data related to the Study in addition to Adaptimmune's final monitoring visit. All reasonable fees associated with the wind-down activities and final monitoring visit shall be paid by Adaptimmune, to the extent not covered by Alliance Funding.
Section 10.1 Misaligned Terminology - In Text Contradiction: Adaptimmune shall assume responsibility for reasonable medical expenses incurred by a Study subject for reasonable and necessary treatment if the Study subject experiences an illness, adverse event or injury that is a result of the Study Drug or any procedure required by the Protocol that the subject would not have undergone were it not for such Study subject's participation in the Study. Adaptimmune shall not be responsible for expenses to the extent that they are due to pre-existing medical conditions, underlying disease, or the negligence or intentional misconduct or due to breach of this Agreement by MD Anderson or Principal Investigator.

Answer:
[
  {
    "section": "Adaptimmune agrees to commit funding in an amount of at least nineteen million six hundred and forty four thousand Dollars US ($19,644,000) for the performance of the Studies as set out in Exhibit I during the term (\"Alliance Funding\"). The JSC may allocate and/or re-allocate funds to Studies as necessary and agreed by JSC.",
    "explanation": "This introduces ambiguity and contradiction by changing 'allocate and/or re-allocate funds to Studies as necessary and agreed by JSC' to 'adjust funds to Studies as necessary', granting the JSC unilateral control without requiring agreement from both parties. This creates uncertainty about whether Adaptimmune has a say in how the funds are spent.",
    "location": "1.3",
    "category": 5
  },
  {
    "section": "The Parties agree that any termination of a Study Order shall allow for: (i) the wind down of the Study to ensure the safety of Study subjects; and (ii) Adaptimmune's final reconciliation of Data related to the Study in addition to Adaptimmune's final monitoring visit. All reasonable fees associated with the wind-down activities and final monitoring visit shall be paid by Adaptimmune, to the extent not covered by Alliance Funding.",
    "explanation": "This change creates a contradiction regarding who is responsible for the fees associated with winding down a study. The original text states that Adaptimmune pays 'all reasonable fees...to the extent not covered by Alliance Funding', whereas the modified text states that all fees are split equally by Adaptimmune and MD Anderson 'regardless of Alliance Funding.' This uncertainty could lead to disputes.",
    "location": "8.3",
    "category": 5
  },
  {
    "section": "Adaptimmune shall assume responsibility for reasonable medical expenses incurred by a Study subject for reasonable and necessary treatment if the Study subject experiences an illness, adverse event or injury that is a result of the Study Drug or any procedure required by the Protocol that the subject would not have undergone were it not for such Study subject's participation in the Study. Adaptimmune shall not be responsible for expenses to the extent that they are due to pre-existing medical conditions, underlying disease, or the negligence or intentional misconduct or due to breach of this Agreement by MD Anderson or Principal Investigator.",
    "explanation": "This modifies 'shall assume responsibility' to 'may, at its sole discretion, cover', which introduces ambiguity regarding Adaptimmune's obligation to cover medical expenses. In original text, it's a requirement but in the changed one, it is up to Adaptimmune's decision. This contradiction creates uncertainty about patient care costs.",
    "location": "10.1",
    "category": 5
  }
]

Question:
Section 7.2 Omissions - In Text Contradiction: Patient records, research notebooks, all original source documents, Protected Health Information (as such term is defined by HIPAA), MD Anderson's business records, regulatory and compliance documents, original medical records or any information required to be maintained by MD Anderson in accordance with Applicable Laws, that is generated in the conduct of the Studies (collectively, "MD Anderson Records") will be owned by MD Anderson. All results, data and work product (excluding MD Anderson Records) generated in the conduct of the Studies ("Data") shall be owned by Adaptimmune Limited. MD Anderson shall maintain all such Data as confidential, subject to the publication rights granted in Section 12 below. Data will be promptly disclosed by MD Anderson to Adaptimmune in the form of a Study report or as otherwise reasonably requested by Adaptimmune. Notwithstanding any other provision of this Agreement, MD Anderson shall have the right to use results and Data of the Study for its internal research, academic, and patient care purposes and for publication in accordance with Section 12 below, save that no right or license is granted to MD Anderson under any of Adaptimmune's Background IP. Adaptimmune shall promptly disclose any Data it generates to MD Anderson.
Section 8.3 Omissions - In Text Contradiction: A Party may terminate a Study Order: (a) if the other Party commits a material breach of this Agreement or the Study Order and fails to cure such breach within thirty (30) days of receiving notice from the non-breaching Party of such breach; or (b) in the case of any Clinical Studies, due to health and safety concerns related to the Study Drug or procedures in the Study (including regulatory holds due to the health and safety of the Study Subjects); or (c) in the case of MD Anderson and in relation to any Clinical Studies, where IRB requests termination of any Study; or (d) in the case of Adaptimmune, *** set out in Section 1.2 above. The Parties agree that any termination of a Study Order shall allow for: (i) the wind down of the Study to ensure the safety of Study subjects; and (ii) Adaptimmune's final reconciliation of Data related to the Study in addition to Adaptimmune's final monitoring visit. All reasonable fees associated with the wind-down activities and final monitoring visit shall be paid by Adaptimmune, to the extent not covered by Alliance Funding. Termination of one or more Study Orders will not automatically result in the termination of this Agreement or termination of any other Study Orders. Upon termination of a Study Order, MD Anderson will immediately return (at Adaptimmune's cost) any Study Drugs provided by Adaptimmune for such Study as directed by Adaptimmune.
Section 12.2 Omissions - In Text Contradiction: Clinical Studies: In relation to any Clinical Study, Adaptimmune shall have the *** right to publish or publicly disclose any Data or results arising from such Clinical Study including where such publication arises from the submission of data and/or results to the regulatory authorities. Such right to publish shall not include any MD Anderson Records or any public health information protected by HIPAA or where any publication would be in breach of the Consent and/or Authorization. MD Anderson and/or Principal Investigator shall have the right to independently publish or publicly disclose, either in writing or orally, the Data and results of the Clinical Study/ies after the earlier of the (i) first publication (including any multi-site publication) of such Data and/or results; (ii) twelve (12) months after completion of any multi-site study encompassing any Study or if none, six (6) months after completion of Study. MD Anderson shall, at least thirty (30) days ahead of any proposed date for submission, furnish Adaptimmune with a written copy of the proposed publication or public disclosure. Within such thirty (30) day period, Adaptimmune shall review such proposed publication for any Confidential Information of Adaptimmune provided hereunder or patentable Data. Adaptimmune may also comment on such proposed publication and MD Anderson shall consider such comments in good faith during the aforementioned thirty (30) day period. MD Anderson and/or Principal Investigator shall remove Confidential Information of Adaptimmune provided hereunder that has been so identified (other than Data or Study results), provided that Adaptimmune agrees to act in good faith when requiring the deletion of Adaptimmune Confidential Information. In addition Adaptimmune may request delay of publication for a period not to exceed *** (***) days from the date of receipt of request by MD Anderson, to permit Adaptimmune or Adaptimmune Limited or any Joint Research Partner to file patent applications or to otherwise seek to protect any intellectual property rights contained in such publication or disclosure. Upon such request, MD Anderson shall delay such publication until the relevant protection is filed up to a maximum of *** (***) days from date of receipt of request for delay by MD Anderson.

Answer:
[
  {
    "section": "Patient records, research notebooks, all original source documents, Protected Health Information (as such term is defined by HIPAA), MD Anderson's business records, regulatory and compliance documents, original medical records or any information required to be maintained by MD Anderson in accordance with Applicable Laws, that is generated in the conduct of the Studies (collectively, \"MD Anderson Records\") will be owned by MD Anderson. All results, data and work product (excluding MD Anderson Records) generated in the conduct of the Studies (\"Data\") shall be owned by Adaptimmune Limited. MD Anderson shall maintain all such Data as confidential, subject to the publication rights granted in Section 12 below. Data will be promptly disclosed by MD Anderson to Adaptimmune in the form of a Study report or as otherwise reasonably requested by Adaptimmune. Notwithstanding any other provision of this Agreement, MD Anderson shall have the right to use results and Data of the Study for its internal research, academic, and patient care purposes and for publication in accordance with Section 12 below, save that no right or license is granted to MD Anderson under any of Adaptimmune's Background IP. Adaptimmune shall promptly disclose any Data it generates to MD Anderson.",
    "explanation": "By removing the section 'Protected Health Information (as such term is defined by HIPAA)', this creates an uncertainty on how to treat this information as it could now be considered 'Data', which is owned by Adaptimmune Limited. This would make the treatment of PHI ambiguous and could lead to breaches of HIPAA if Adaptimmune treats it as regular data.",
    "location": "7.2",
    "category": 7
  },
  {
    "section": "A Party may terminate a Study Order: (a) if the other Party commits a material breach of this Agreement or the Study Order and fails to cure such breach within thirty (30) days of receiving notice from the non-breaching Party of such breach; or (b) in the case of any Clinical Studies, due to health and safety concerns related to the Study Drug or procedures in the Study (including regulatory holds due to the health and safety of the Study Subjects); or (c) in the case of MD Anderson and in relation to any Clinical Studies, where IRB requests termination of any Study; or (d) in the case of Adaptimmune, *** set out in Section 1.2 above. The Parties agree that any termination of a Study Order shall allow for: (i) the wind down of the Study to ensure the safety of Study subjects; and (ii) Adaptimmune's final reconciliation of Data related to the Study in addition to Adaptimmune's final monitoring visit. All reasonable fees associated with the wind-down activities and final monitoring visit shall be paid by Adaptimmune, to the extent not covered by Alliance Funding. Termination of one or more Study Orders will not automatically result in the termination of this Agreement or termination of any other Study Orders. Upon termination of a Study Order, MD Anderson will immediately return (at Adaptimmune's cost) any Study Drugs provided by Adaptimmune for such Study as directed by Adaptimmune.",
    "explanation": "The section '(d) in the case of Adaptimmune, *** set out in Section 1.2 above' contains an omission already in the original contract. By removing the asterisks, it suggests that Adaptimmune does have a unilateral right to terminate, but the grounds are unknown because the text is still omitted as the text references Section 1.2 above. Thus Section 1.2 is an essential condition for Adaptimmune to terminate, but the details are omitted.",
    "location": "8.3",
    "category": 7
  },
  {
    "section": "Clinical Studies: In relation to any Clinical Study, Adaptimmune shall have the *** right to publish or publicly disclose any Data or results arising from such Clinical Study including where such publication arises from the submission of data and/or results to the regulatory authorities. Such right to publish shall not include any MD Anderson Records or any public health information protected by HIPAA or where any publication would be in breach of the Consent and/or Authorization. MD Anderson and/or Principal Investigator shall have the right to independently publish or publicly disclose, either in writing or orally, the Data and results of the Clinical Study/ies after the earlier of the (i) first publication (including any multi-site publication) of such Data and/or results; (ii) twelve (12) months after completion of any multi-site study encompassing any Study or if none, six (6) months after completion of Study. MD Anderson shall, at least thirty (30) days ahead of any proposed date for submission, furnish Adaptimmune with a written copy of the proposed publication or public disclosure. Within such thirty (30) day period, Adaptimmune shall review such proposed publication for any Confidential Information of Adaptimmune provided hereunder or patentable Data. Adaptimmune may also comment on such proposed publication and MD Anderson shall consider such comments in good faith during the aforementioned thirty (30) day period. MD Anderson and/or Principal Investigator shall remove Confidential Information of Adaptimmune provided hereunder that has been so identified (other than Data or Study results), provided that Adaptimmune agrees to act in good faith when requiring the deletion of Adaptimmune Confidential Information. In addition Adaptimmune may request delay of publication for a period not to exceed *** (***) days from the date of receipt of request by MD Anderson, to permit Adaptimmune or Adaptimmune Limited or any Joint Research Partner to file patent applications or to otherwise seek to protect any intellectual property rights contained in such publication or disclosure. Upon such request, MD Anderson shall delay such publication until the relevant protection is filed up to a maximum of *** (***) days from date of receipt of request for delay by MD Anderson.",
    "explanation": "In the original text, there are asterisks indicating that some wording is omitted, which means that there is a term that is not defined. In the changed text, the asterisks have been removed from 'Adaptimmune shall have the *** right to publish'. By removing this asterisks, it implies that Adaptimmune can publish or publicly disclose any data, giving them full rights. However, the type or extent of these rights is not defined, creating uncertainty.",
    "location": "12.2",
    "category": 7
  }
]

Question: [DOCUMENT]
Answer:
"""