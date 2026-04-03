"""
Gemini AI Agent Code Review for Email Phishing Detection Project
This script uses Google Gemini API to perform comprehensive code reviews
on the phishing detection project from AI_Detection_6.
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from AI_Detection_6 folder
env_path = Path(__file__).parent / 'AI_Detection_6' / '.env'
load_dotenv(env_path)

class GeminiCodeReviewer:
    """AI Agent for comprehensive code review using Gemini API"""

    def __init__(self):
        """Initialize Gemini API"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.reviews = []

        # Configure for detailed analysis
        self.generation_config = {
            'temperature': 0.3,  # Balanced for thoughtful analysis
            'top_p': 0.95,
            'max_output_tokens': 8192,  # Allow for comprehensive reviews
        }

    def read_project_files(self, base_path):
        """Read key project files for review"""
        files_to_read = {
            'README.md': 'README.md',
            'phishing_detector.py': 'phishing_detector.py',
            'api_server.py': 'api_server.py',
            'evaluate_model.py': 'evaluate_model.py',
            'test_detector.py': 'test_detector.py',
            'requirements.txt': 'requirements.txt',
            'extension/manifest.json': 'extension/manifest.json',
            'extension/popup.js': 'extension/popup.js'
        }

        project_content = {}
        for key, filepath in files_to_read.items():
            full_path = os.path.join(base_path, filepath)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    project_content[key] = f.read()
            except FileNotFoundError:
                project_content[key] = f"File not found: {filepath}"
            except Exception as e:
                project_content[key] = f"Error reading file: {str(e)}"

        return project_content

    def run_review(self, prompt_name, prompt_text, context=""):
        """Execute a single code review prompt"""
        print(f"\n{'='*80}")
        print(f"Running Review: {prompt_name}")
        print(f"{'='*80}\n")

        full_prompt = f"{prompt_text}\n\n{context}" if context else prompt_text

        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config=self.generation_config
            )

            review_result = {
                'prompt_name': prompt_name,
                'timestamp': datetime.now().isoformat(),
                'response': response.text,
                'success': True
            }

            print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
            print(f"\n[Review completed - {len(response.text)} characters]")

            # Rate limiting
            time.sleep(2)

        except Exception as e:
            review_result = {
                'prompt_name': prompt_name,
                'timestamp': datetime.now().isoformat(),
                'response': f"Error: {str(e)}",
                'success': False
            }
            print(f"ERROR: {str(e)}")

        self.reviews.append(review_result)
        return review_result

    def save_reviews(self, output_file='code_review_results.json'):
        """Save all reviews to JSON file"""
        output = {
            'project': 'Email Phishing Detection - AI_Detection_6',
            'review_date': datetime.now().isoformat(),
            'total_reviews': len(self.reviews),
            'reviews': self.reviews
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"\n\nAll reviews saved to: {output_file}")
        return output_file


def main():
    """Execute comprehensive code review"""

    print("="*80)
    print("GEMINI AI AGENT - PHISHING DETECTION PROJECT CODE REVIEW")
    print("="*80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

    # Initialize reviewer
    reviewer = GeminiCodeReviewer()

    # Read project files
    project_path = Path(__file__).parent / 'AI_Detection_6'
    print(f"Reading project files from: {project_path}\n")
    project_files = reviewer.read_project_files(project_path)

    # Prepare file context for reviews
    code_context = f"""
# Project Files for Review:

## README.md (First 2000 chars)
{project_files['README.md'][:2000]}

## phishing_detector.py
{project_files['phishing_detector.py']}

## api_server.py
{project_files['api_server.py']}

## evaluate_model.py
{project_files['evaluate_model.py']}

## requirements.txt
{project_files['requirements.txt']}

## extension/manifest.json
{project_files['extension/manifest.json']}
"""

    # Define comprehensive review prompts based on assignment requirements

    # REVIEW 1: High-Level Project Overview
    reviewer.run_review(
        "1. High-Level Project Overview",
        """You are an expert cybersecurity ML engineer. Analyze this entire GitHub repository for an email phishing detection project.

Summarize:
1. The architecture and overall approach
2. Technologies used (frameworks, APIs, libraries)
3. Data pipeline and workflow
4. Model choices and reasoning
5. Main strengths of the implementation
6. Obvious gaps or missing components

Provide a comprehensive overview in 400-600 words.""",
        code_context
    )

    # REVIEW 2: Code Quality & Best Practices
    reviewer.run_review(
        "2. Code Quality & Best Practices",
        """Act as a senior code reviewer. Review the codebase for:

1. **Readability & Modularity**:
   - Code organization and structure
   - Function/class design
   - Separation of concerns

2. **Python Best Practices**:
   - PEP 8 compliance
   - Naming conventions
   - Code documentation and comments

3. **Error Handling**:
   - Exception handling quality
   - Edge case coverage
   - Graceful failure mechanisms

4. **Specific Issues**:
   - Problematic file paths or hardcoded values
   - Configuration management
   - Dependencies and version control

Point out specific code sections with line references and provide concrete suggestions for improvement.""",
        code_context
    )

    # REVIEW 3: ML Model & Performance Review
    reviewer.run_review(
        "3. ML Model & Performance Review (CRITICAL FOR PHISHING PROJECTS)",
        """Evaluate the machine learning pipeline for phishing email detection:

1. **Data Preprocessing**:
   - How is email text cleaned and prepared?
   - Data validation and sanitization

2. **Feature Engineering**:
   - Text features (TF-IDF, embeddings, etc.)
   - URL/link analysis features
   - Sender/domain features
   - What's missing?

3. **Imbalanced Classes**:
   - How is class imbalance handled?
   - Appropriate metrics for imbalanced data?

4. **Model Training & Evaluation**:
   - Model selection justification
   - Evaluation metrics (accuracy, precision, RECALL - critical for security)
   - Risk of overfitting
   - Cross-validation strategy

5. **Phishing Detection Effectiveness**:
   - Can it detect sophisticated phishing emails?
   - False negative rate (missing real threats)
   - False positive rate (blocking legitimate emails)

6. **Improvement Suggestions**:
   - Better features to extract
   - Ensemble methods
   - Transfer learning opportunities
   - Model calibration

Provide detailed technical analysis with specific recommendations.""",
        code_context
    )

    # REVIEW 4: Security & Vulnerability Audit
    reviewer.run_review(
        "4. Security & Vulnerability Audit (CRITICAL AREA)",
        """Perform a security-focused review. Look for:

1. **Secrets Management**:
   - Hardcoded API keys, passwords, or tokens
   - Environment variable handling
   - .env file security

2. **Input Validation & Sanitization**:
   - Unsafe handling of raw email content
   - SQL injection vulnerabilities
   - Command injection risks
   - XSS vulnerabilities in web components

3. **API Security**:
   - CORS configuration appropriateness
   - Authentication/authorization
   - Rate limiting
   - Input validation on endpoints

4. **Dependency Vulnerabilities**:
   - Outdated or vulnerable packages
   - Missing security patches

5. **Model Security**:
   - Risk of model poisoning
   - Prompt injection vulnerabilities (if using LLMs)
   - Adversarial attack resilience

6. **Privacy & Data Protection**:
   - How is sensitive email data handled?
   - Data retention policies
   - Logging of sensitive information

For each vulnerability found, rate severity (CRITICAL/HIGH/MEDIUM/LOW) and provide remediation steps.""",
        code_context
    )

    # REVIEW 5: Phishing-Specific Techniques & Edge Cases
    reviewer.run_review(
        "5. Phishing-Specific Techniques & Edge Cases",
        """As a phishing detection specialist, analyze how well this project handles:

1. **Common Phishing Tactics**:
   - Urgency language ("Act now!", "Account suspended")
   - Spoofed senders (display name vs. email mismatch)
   - Malicious links (typosquatting, URL shorteners)
   - Social engineering techniques

2. **Advanced Phishing Techniques**:
   - Business Email Compromise (BEC)
   - CEO fraud / whaling
   - Spear phishing (targeted attacks)
   - Clone phishing
   - Homograph attacks (unicode lookalikes)

3. **Edge Cases**:
   - Legitimate urgent emails (password resets, security alerts)
   - International/non-English phishing
   - Image-based phishing (if applicable)
   - Embedded links vs. attachments

4. **Detection Robustness**:
   - Handling of obfuscated text
   - Zero-day phishing campaigns
   - Evolving threat landscape adaptation

5. **Recommendations**:
   - Additional NLP techniques (sentiment analysis, entity recognition)
   - URL reputation checking integration
   - Header analysis (DMARC, SPF, DKIM)
   - Behavioral analysis
   - Ensemble methods combining multiple signals

Suggest 5-7 concrete improvements to make the detector more robust against evolving phishing threats.""",
        code_context
    )

    # REVIEW 6: Documentation, Reproducibility & Deployment
    reviewer.run_review(
        "6. Documentation, Reproducibility & Deployment",
        """Review documentation and deployment readiness:

1. **README Quality**:
   - Clarity and completeness
   - Installation instructions
   - Usage examples
   - Troubleshooting guide

2. **Code Documentation**:
   - Docstrings completeness
   - Inline comments appropriateness
   - API documentation

3. **Reproducibility**:
   - requirements.txt completeness
   - Version pinning strategy
   - Dataset access and preparation
   - Environment setup automation

4. **Deployment Considerations** (if applicable):
   - Production readiness of Flask API
   - Scalability concerns
   - Monitoring and logging
   - CI/CD pipeline suggestions
   - Security hardening for production

5. **Browser Extension**:
   - Extension manifest quality
   - User experience considerations
   - Permissions justification
   - Cross-browser compatibility

6. **Enhancements**:
   - What's missing from documentation?
   - How to improve reproducibility?
   - Deployment automation suggestions

Rate documentation quality (1-10) and provide specific improvements.""",
        code_context
    )

    # REVIEW 7: Ethical & Responsible AI Review
    reviewer.run_review(
        "7. Ethical & Responsible AI Review",
        """Discuss ethical considerations for this phishing detection tool:

1. **Bias & Fairness**:
   - Potential biases in training data
   - False positive impact on legitimate communications
   - Fairness across different user groups
   - Language/cultural biases

2. **Privacy Concerns**:
   - Email content being sent to external API (Google Gemini)
   - User consent and transparency
   - Data retention and privacy policy
   - GDPR/privacy regulation compliance

3. **Responsible Use**:
   - Misuse prevention measures
   - Clear defensive security purpose
   - Dual-use concerns
   - Limitations clearly communicated

4. **Transparency & Explainability**:
   - Are decisions explainable to users?
   - SHAP/LIME integration suggestions
   - User education vs. just blocking

5. **Accountability**:
   - What happens when the tool fails?
   - User recourse for false positives
   - Continuous monitoring and updates

6. **Social Impact**:
   - Accessibility considerations
   - Digital literacy implications
   - Potential for over-reliance on automation

Provide 5-7 concrete recommendations for making this project more ethical and responsible.""",
        code_context
    )

    # REVIEW 8: Improvement Agent Task
    reviewer.run_review(
        "8. Improvement Agent - Concrete Enhancement Proposals",
        """You are a refactoring and enhancement agent. Propose 5-7 concrete improvements with:

For each improvement:
1. **Title**: Clear improvement name
2. **Rationale**: Why this matters for phishing detection
3. **Impact**: Expected improvement in accuracy, security, or UX
4. **Implementation Sketch**: High-level code approach (pseudocode acceptable)
5. **Effort Estimate**: Low/Medium/High complexity
6. **Priority**: Critical/High/Medium/Low

Focus on improvements that:
- Increase detection accuracy
- Reduce false negatives (missed threats)
- Enhance security
- Improve user experience
- Make the system more robust

Provide actionable, specific proposals that could be implemented in a future version.""",
        code_context
    )

    # Save all reviews
    output_file = reviewer.save_reviews('code_review_results.json')

    print("\n" + "="*80)
    print("CODE REVIEW COMPLETE")
    print("="*80)
    print(f"Total Reviews: {len(reviewer.reviews)}")
    print(f"Successful: {sum(1 for r in reviewer.reviews if r['success'])}")
    print(f"Failed: {sum(1 for r in reviewer.reviews if not r['success'])}")
    print(f"Output File: {output_file}")
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

    return reviewer.reviews


if __name__ == "__main__":
    try:
        reviews = main()
        print("\nNext Steps:")
        print("1. Review the output file: code_review_results.json")
        print("2. Create screenshots of key findings")
        print("3. Write critical reflection based on AI feedback")
        print("4. Compile final report with evidence, analysis, and action plan")
    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
        sys.exit(1)
