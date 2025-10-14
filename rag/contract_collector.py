"""
Contract Collector - Creates a database of standard contracts
Since we can't scrape real contracts easily, we'll generate realistic templates
based on common contract patterns
"""

import os
from typing import List, Dict
import json


class ContractCollector:
    """
    Generates standard contract templates for comparison database
    """
    
    def __init__(self, output_dir: str = "rag/contract_database"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_standard_contracts(self):
        """
        Generate a collection of fair, standard contract templates
        These represent industry best practices
        """
        contracts = [
            self._generate_fair_freelance_contract(),
            self._generate_fair_employment_contract(),
            self._generate_fair_nda(),
            self._generate_fair_saas_agreement(),
            self._generate_fair_consulting_agreement(),
            self._generate_contractor_agreement_variant1(),
            self._generate_contractor_agreement_variant2(),
            self._generate_nda_variant1(),
            self._generate_nda_variant2(),
        ]
        
        # Save each contract
        for i, contract in enumerate(contracts, 1):
            filename = f"{contract['type'].lower().replace(' ', '_')}_{i}.json"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(contract, f, indent=2)
            
            print(f"Generated: {filename}")

        print(f"\nCreated {len(contracts)} standard contracts in {self.output_dir}")
        return contracts
    
    def _generate_fair_freelance_contract(self) -> Dict:
        """Standard freelance contract - fair terms"""
        # Note: 'risk_level' is a contract-level key, not a clause-level key.
        return {
            "type": "Freelance Agreement",
            "risk_level": "low",
            "description": "Industry standard freelance services agreement",
            "clauses": {
                "termination": {
                    "text": "Either party may terminate this Agreement with thirty (30) days written notice. Upon termination, Client shall pay Freelancer for all work completed through the termination date.",
                    "key_terms": {
                        "notice_period_days": 30,
                        "notice_required_by": "both parties",
                        "payment_on_termination": "for work completed",
                        "fairness_score": 9
                    },
                    "benchmark": "30 days is standard across industry"
                },
                "payment": {
                    "text": "Client agrees to pay Freelancer the fees specified in Statement of Work, payable within fifteen (15) business days of invoice receipt. Late payments accrue interest at 1.5% per month.",
                    "key_terms": {
                        "payment_terms_days": 15,
                        "late_fee": "1.5% per month",
                        "payment_contingency": "none",
                        "fairness_score": 9
                    },
                    "benchmark": "Net-15 to Net-30 is standard"
                },
                "intellectual_property": {
                    "text": "Upon receipt of full payment, Freelancer grants Client all rights to final deliverables. Freelancer retains rights to preliminary work, techniques, and may use completed work in portfolio with Client approval.",
                    "key_terms": {
                        "transfer_trigger": "upon full payment",
                        "scope": "final deliverables only",
                        "freelancer_retains": "preliminary work, techniques, portfolio rights",
                        "fairness_score": 8
                    },
                    "benchmark": "Transfer on payment is fair; portfolio rights standard"
                },
                "liability": {
                    "text": "Each party's total liability shall not exceed the total fees paid under this Agreement. Neither party liable for indirect or consequential damages.",
                    "key_terms": {
                        "cap": "fees paid",
                        "mutual": True,
                        "excludes_consequential": True,
                        "fairness_score": 8
                    },
                    "benchmark": "Capped, mutual liability is standard"
                },
                "non_compete": {
                    "text": "During the term, Freelancer agrees not to provide substantially similar services to direct competitors within the same geographic market.",
                    "key_terms": {
                        "duration_months": 0,  # Only during term
                        "geographic_scope": "same market",
                        "scope": "direct competitors only",
                        "post_termination": False,
                        "fairness_score": 9
                    },
                    "benchmark": "Limited to term only is fair; post-term restrictions should be 6-12 months max"
                },
                "revisions": {
                    "text": "Client entitled to two (2) rounds of reasonable revisions per deliverable. Additional revisions billed at standard hourly rate.",
                    "key_terms": {
                        "included_revisions": 2,
                        "additional_cost": "hourly rate",
                        "fairness_score": 9
                    },
                    "benchmark": "2-3 revision rounds is industry standard"
                }
            }
        }
    
    def _generate_fair_employment_contract(self) -> Dict:
        """Standard employment agreement"""
        return {
            "type": "Employment Agreement",
            "risk_level": "low",
            "description": "Standard full-time employment contract",
            "clauses": {
                "termination": {
                    "text": "Either party may terminate employment with sixty (60) days written notice. In case of termination by Employer without cause, Employee entitled to sixty (60) days severance pay.",
                    "key_terms": {
                        "notice_period_days": 60,
                        "severance": "60 days pay",
                        "fairness_score": 8
                    },
                    "benchmark": "60-90 days notice with severance is standard"
                },
                "compensation": {
                    "text": "Employee shall receive annual salary of $[Amount], paid bi-weekly. Eligible for annual performance bonus up to 15% of base salary.",
                    "key_terms": {
                        "payment_schedule": "bi-weekly",
                        "bonus_potential": "15%",
                        "fairness_score": 9
                    },
                    "benchmark": "Bi-weekly pay is standard; 10-20% bonus typical"
                },
                "intellectual_property": {
                    "text": "Employee assigns to Employer all rights to work created within scope of employment. Personal projects created on own time with own resources remain Employee's property.",
                    "key_terms": {
                        "scope": "within employment duties",
                        "personal_projects_protected": True,
                        "fairness_score": 8
                    },
                    "benchmark": "Work-related IP to employer; personal projects protected"
                },
                "non_compete": {
                    "text": "For twelve (12) months after termination, Employee agrees not to work for direct competitors in same role within 50-mile radius.",
                    "key_terms": {
                        "duration_months": 12,
                        "geographic_scope": "50 miles",
                        "scope": "direct competitors, same role",
                        "fairness_score": 7
                    },
                    "benchmark": "12 months is reasonable; should be limited geographically and by role"
                }
            }
        }
    
    def _generate_fair_nda(self) -> Dict:
        """Standard NDA"""
        return {
            "type": "Non-Disclosure Agreement",
            "risk_level": "low",
            "description": "Mutual NDA with balanced terms",
            "clauses": {
                "term": {
                    "text": "This Agreement shall remain in effect for two (2) years from the Effective Date. Confidentiality obligations survive termination for two (2) additional years.",
                    "key_terms": {
                        "agreement_term_years": 2,
                        "confidentiality_survival_years": 2,
                        "total_obligation_years": 4,
                        "fairness_score": 9
                    },
                    "benchmark": "2-3 year term with 2-5 year survival is standard"
                },
                "scope": {
                    "text": "Confidential Information means non-public information marked confidential or that reasonably should be understood as confidential. Excludes information that is publicly available, independently developed, or rightfully obtained from third parties.",
                    "key_terms": {
                        "definition": "clear and reasonable",
                        "exclusions": "standard exclusions included",
                        "fairness_score": 9
                    },
                    "benchmark": "Clear definition with standard exclusions is fair"
                },
                "obligations": {
                    "text": "Receiving Party shall use same degree of care to protect Confidential Information as it uses for its own confidential information, but no less than reasonable care.",
                    "key_terms": {
                        "standard_of_care": "reasonable care",
                        "mutual": True,
                        "fairness_score": 9
                    },
                    "benchmark": "Reasonable care standard is fair and enforceable"
                },
                "remedies": {
                    "text": "Breach may cause irreparable harm. Disclosing Party entitled to seek injunctive relief in addition to other remedies.",
                    "key_terms": {
                        "injunctive_relief": True,
                        "monetary_damages": True,
                        "fairness_score": 8
                    },
                    "benchmark": "Standard remedy provisions for NDAs"
                }
            }
        }
    
    def _generate_fair_saas_agreement(self) -> Dict:
        """Standard SaaS service agreement"""
        return {
            "type": "SaaS Agreement",
            "risk_level": "low",
            "description": "Standard software-as-a-service terms",
            "clauses": {
                "term": {
                    "text": "Initial term of twelve (12) months, automatically renewing for successive twelve (12) month periods unless either party provides sixty (60) days notice of non-renewal.",
                    "key_terms": {
                        "initial_term_months": 12,
                        "auto_renewal": True,
                        "cancellation_notice_days": 60,
                        "fairness_score": 8
                    },
                    "benchmark": "Annual terms with 30-60 day cancellation notice is standard"
                },
                "fees": {
                    "text": "Customer shall pay annual subscription fee as specified in Order Form. Fees may increase by up to 5% annually with ninety (90) days notice.",
                    "key_terms": {
                        "payment_frequency": "annual",
                        "price_increase_cap": "5% per year",
                        "price_increase_notice_days": 90,
                        "fairness_score": 8
                    },
                    "benchmark": "Capped price increases with notice is fair"
                },
                "data_ownership": {
                    "text": "Customer retains all ownership rights to Customer Data. Provider has limited license to use Customer Data solely to provide Services.",
                    "key_terms": {
                        "customer_owns_data": True,
                        "provider_license": "limited to service provision",
                        "fairness_score": 10
                    },
                    "benchmark": "Customer data ownership is essential"
                },
                "liability": {
                    "text": "Provider's total liability shall not exceed fees paid in the twelve (12) months prior to the claim. Neither party liable for indirect, incidental, or consequential damages.",
                    "key_terms": {
                        "cap": "12 months of fees",
                        "excludes_consequential": True,
                        "fairness_score": 7
                    },
                    "benchmark": "12-month fee cap is standard for SaaS"
                }
            }
        }
    
    def _generate_fair_consulting_agreement(self) -> Dict:
        """Standard consulting agreement"""
        return {
            "type": "Consulting Agreement",
            "risk_level": "low",
            "description": "Professional services consulting agreement",
            "clauses": {
                "termination": {
                    "text": "Either party may terminate with forty-five (45) days written notice. Client shall pay for all services rendered through termination date.",
                    "key_terms": {
                        "notice_period_days": 45,
                        "payment_on_termination": "for services rendered",
                        "fairness_score": 8
                    },
                    "benchmark": "30-60 days notice is standard for consulting"
                },
                "payment": {
                    "text": "Client pays Consultant at rates specified in Statement of Work, invoiced monthly. Payment due within thirty (30) days of invoice date.",
                    "key_terms": {
                        "payment_terms_days": 30,
                        "invoicing_frequency": "monthly",
                        "fairness_score": 8
                    },
                    "benchmark": "Net-30 is standard for B2B consulting"
                },
                "expenses": {
                    "text": "Client reimburses pre-approved reasonable business expenses within fifteen (15) days of receipt of expense report with supporting documentation.",
                    "key_terms": {
                        "reimbursement": "pre-approved expenses",
                        "reimbursement_terms_days": 15,
                        "fairness_score": 9
                    },
                    "benchmark": "Expense reimbursement is standard"
                }
            }
        }
    
    def _generate_contractor_agreement_variant1(self) -> Dict:
        """Variant of contractor agreement with slightly different terms"""
        return {
            "type": "Contractor Agreement",
            "risk_level": "low",
            "description": "Independent contractor agreement - variant 1",
            "clauses": {
                "termination": {
                    "text": "Either party may terminate this Agreement with fourteen (14) days written notice for convenience, or immediately for material breach.",
                    "key_terms": {
                        "notice_period_days": 14,
                        "immediate_termination": "material breach only",
                        "fairness_score": 7
                    },
                    "benchmark": "14 days is acceptable for short-term contracts; 30+ days better for long-term"
                },
                "payment": {
                    "text": "Contractor invoices upon milestone completion. Client pays within twenty (20) business days. Late payments accrue 2% monthly interest.",
                    "key_terms": {
                        "payment_terms_days": 20,
                        "payment_trigger": "milestone completion",
                        "late_fee": "2% per month",
                        "fairness_score": 8
                    },
                    "benchmark": "Milestone-based payment is common and fair"
                }
            }
        }
    
    def _generate_contractor_agreement_variant2(self) -> Dict:
        """Another contractor variant"""
        return {
            "type": "Contractor Agreement",
            "risk_level": "low",
            "description": "Independent contractor agreement - variant 2",
            "clauses": {
                "intellectual_property": {
                    "text": "All work product specifically created for Client under this Agreement becomes Client property upon final payment. Contractor retains rights to pre-existing materials and general knowledge.",
                    "key_terms": {
                        "transfer_trigger": "upon final payment",
                        "scope": "work specifically created for client",
                        "contractor_retains": "pre-existing materials, general knowledge",
                        "fairness_score": 9
                    },
                    "benchmark": "Transfer on payment with retained general knowledge is fair"
                },
                "warranty": {
                    "text": "Contractor warrants work will be performed in professional and workmanlike manner. Contractor will correct any defects in work for ninety (90) days after delivery at no additional charge.",
                    "key_terms": {
                        "warranty_period_days": 90,
                        "warranty_scope": "professional quality",
                        "correction_cost": "no additional charge",
                        "fairness_score": 8
                    },
                    "benchmark": "90-day workmanship warranty is standard"
                }
            }
        }
    
    def _generate_nda_variant1(self) -> Dict:
        """NDA variant"""
        return {
            "type": "Non-Disclosure Agreement",
            "risk_level": "low",
            "description": "Standard NDA - variant 1",
            "clauses": {
                "term": {
                    "text": "This Agreement effective from Effective Date and continues for three (3) years. Confidentiality obligations survive for three (3) years after termination.",
                    "key_terms": {
                        "agreement_term_years": 3,
                        "confidentiality_survival_years": 3,
                        "fairness_score": 8
                    },
                    "benchmark": "3+3 years is reasonable for most business relationships"
                },
                "permitted_disclosure": {
                    "text": "Receiving Party may disclose to employees, contractors, and advisors with legitimate need to know, provided they are bound by confidentiality obligations.",
                    "key_terms": {
                        "permitted_recipients": "employees, contractors, advisors",
                        "requirement": "need to know + confidentiality agreement",
                        "fairness_score": 9
                    },
                    "benchmark": "Reasonable disclosure provisions are necessary"
                }
            }
        }
    
    def _generate_nda_variant2(self) -> Dict:
        """Another NDA variant"""
        return {
            "type": "Non-Disclosure Agreement",
            "risk_level": "low",
            "description": "Standard NDA - variant 2",
            "clauses": {
                "return_of_materials": {
                    "text": "Upon termination or upon request, Receiving Party shall promptly return or destroy all Confidential Information and certify destruction in writing.",
                    "key_terms": {
                        "return_required": True,
                        "destruction_option": True,
                        "certification_required": True,
                        "fairness_score": 9
                    },
                    "benchmark": "Return or destroy with certification is standard"
                },
                "compelled_disclosure": {
                    "text": "If Receiving Party compelled by law to disclose, must notify Disclosing Party promptly to allow seeking protective order. Receiving Party shall cooperate in seeking such order.",
                    "key_terms": {
                        "notice_required": True,
                        "cooperation_required": True,
                        "fairness_score": 9
                    },
                    "benchmark": "Notice provision for legal compulsion is fair"
                }
            }
        }


# Helper function
def create_contract_database():
    """Quick function to generate all standard contracts"""
    collector = ContractCollector()
    return collector.generate_standard_contracts()


if __name__ == "__main__":
    print("Creating standard contract database...")
    print("=" * 60)
    create_contract_database()
    print("\nContract database creation complete!")