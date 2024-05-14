from flask import Flask, render_template, request
import dns.resolver
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)



def get_dns_hosting_provider(domain):
    try:
        dns_records = dns.resolver.resolve(domain, 'NS')
        nameservers = [ns.target.to_text() for ns in dns_records]

        if any('domaincontrol.com' in ns for ns in nameservers):
            return f"Your DNS hosting provider for {domain} is 'GoDaddy'"
        elif any('cloudflare.com' in ns for ns in nameservers):
            return f"Your DNS hosting provider for {domain} is 'Cloudflare'"       
        elif any('google' in ns for ns in nameservers):
            return f"Your DNS hosting provider for {domain} is 'Google'"
        elif any('amazonaws.com' in ns for ns in nameservers):
            return f"Your DNS hosting provider for {domain} is 'Amazon'"
        elif any('awsdns' in ns for ns in nameservers):
            return f"Your DNS hosting provider for {domain} is 'Amazon'"
        elif any('opendns' in ns for ns in nameservers):
            return f"Your DNS hosting provider for {domain} is 'OpenDNS'"
        elif any('azure-dns' in ns for ns in nameservers):
            return f"Your DNS hosting provider for {domain} is 'Azure DNS'"
        elif any('ns1.com' in ns for ns in nameservers):
            return f"Your DNS hosting provider for {domain} is 'IBM NS1'"
        elif any('ns4' in ns for ns in nameservers):
            return f"Your DNS hosting provider for {domain} is 'ns4'"
        else:
            return f"No recognized DNS hosting provider found for {domain}"
    except dns.resolver.NXDOMAIN:
        return None


def dns_hosting_provider(domain):
    try:
        ns_records = dns.resolver.resolve(domain, 'NS')
        hosting_providers = [ns.target.to_text() for ns in ns_records]
        if hosting_providers:
            return f"DNS hosting providers for {domain}: {', '.join(hosting_providers)}"
        else:
            return None
    except dns.resolver.NXDOMAIN:
        return None

def mx_lookup(domain):
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_results = [f"{mx.exchange} (Preference: {mx.preference})" for mx in mx_records]

    except dns.resolver.NXDOMAIN:
        mx_results = None
    return mx_results

def dmarc_lookup(domain):
    try:
        dmarc_records = dns.resolver.resolve(f'_dmarc.{domain}', 'TXT')
        dmarc_results = [f"{record}" for record in dmarc_records]

    except dns.resolver.NXDOMAIN:
        dmarc_results = None
    return dmarc_results

def dkim_lookup(domain):
    try:
        dkim_records = dns.resolver.resolve(f'selector1._domainkey.{domain}', 'TXT')
        dkim_results = [f"{record}" for record in dkim_records]
    except dns.resolver.NXDOMAIN:
        dkim_results = None
    return dkim_results

def spf_lookup(domain):
    try:
        spf_records = dns.resolver.resolve(domain, 'TXT')
        spf_results = [record.strings[0].decode('utf-8') for record in spf_records if record.strings and record.strings[0].startswith(b"v=spf1")]
    except dns.resolver.NXDOMAIN:
        spf_results = None
    return spf_results

def dns_lookup(domain):
    try:
        dns_records = dns.resolver.resolve(domain)
        dns_results = [f"{record}" for record in dns_records]
    except dns.resolver.NXDOMAIN:
        dns_results = None
    return dns_results

def mta_sts_lookup(domain):
    try:
        mta_sts_records = dns.resolver.resolve(f"_mta-sts.{domain}", 'TXT')
        mta_sts_results = [record.strings[0] for record in mta_sts_records]
        return mta_sts_results
    except dns.resolver.NXDOMAIN:
        return None


def txt_lookup(domain):
    try:
        txt_records = dns.resolver.resolve(domain, 'TXT')
        txt_results = [f"{record}" for record in txt_records]
    except dns.resolver.NXDOMAIN:
        txt_results = None
    return txt_results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    domain = request.form['domain']
    mx_results = mx_lookup(domain)
    dmarc_results = dmarc_lookup(domain)
    dkim_results = dkim_lookup(domain)  
    spf_results = spf_lookup(domain)   
    dns_results= dns_lookup(domain)
    mta_sts_results= mta_sts_lookup(domain)
    txt_results = txt_lookup(domain)
    hosting_provider= dns_hosting_provider(domain)
    dns_provider = get_dns_hosting_provider(domain)
    return render_template('results.html', domain=domain, dns_provider=dns_provider, hosting_provider=hosting_provider, txt_results=txt_results, mta_sts_results= mta_sts_results,mx_results=mx_results, dmarc_results=dmarc_results, dkim_results=dkim_results, spf_results=spf_results, dns_results=dns_results)


if __name__ == '__main__':
    app.run(debug=True)
