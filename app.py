import os
import sys
from google import genai

def audit_config(config_text):
    # Automatically loads GEMINI_API_KEY from environment variables
    client = genai.Client()
    
    prompt = f"""
    You are an expert Network Security Engineer. Analyze the following firewall configuration or network log snippet for security vulnerabilities, misconfigurations (such as any-any rules, missing hardening, or insecure policies), and provide a structured markdown remediation report:
    
    {config_text}
    """
    
    print("[*] Analyzing configuration with Gemma 4...")
    response = client.models.generate_content(
        model='gemma-4-31b-it',
        contents=prompt,
    )
    return response.text

if __name__ == "__main__":
    print("=== NetShield Auditor (Powered by Gemma 4) ===")
    
    # Sample default config if no file is provided
    sample_config = """
    config firewall policy
        edit 1
            set name "Allow_All_Outbound"
            set srcintf "internal"
            set dstintf "wan"
            set srcaddr "all"
            set dstaddr "all"
            set action accept
            set schedule "always"
            set service "ALL"
        next
    end
    """
    
    # Check if a config file path was passed as an argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                config_data = f.read()
        else:
            print(f"Error: File {file_path} not found.")
            sys.exit(1)
    else:
        print("[*] No config file provided. Running with sample vulnerable firewall policy...")
        config_data = sample_config
        
    report = audit_config(config_data)
    print("\n" + "="*40 + "\nSECURITY AUDIT REPORT\n" + "="*40)
    print(report)
