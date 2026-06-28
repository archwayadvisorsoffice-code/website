import json
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'archway-dev-secret-2025')

# ── Mail configuration ───────────────────────────────────────────────────────
# Set MAIL_USERNAME and MAIL_PASSWORD as environment variables or in a .env file
app.config['MAIL_SERVER']   = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT']     = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS']  = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)

RECIPIENT_EMAIL = 'info@archway.in'


# ── Load blog data ───────────────────────────────────────────────────────────
def load_blogs():
    path = os.path.join(os.path.dirname(__file__), 'data', 'blogs.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


# ── Template context processor (injects current year everywhere) ─────────────
@app.context_processor
def inject_globals():
    return {'current_year': datetime.now().year}


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    blogs = load_blogs()
    return render_template('index.html', featured_blogs=blogs[:3])


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/why-us')
def why_us():
    return render_template('why-us.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/countries')
def countries():
    return render_template('countries.html')


COUNTRY_DATA = {
    'india': {
        'name': 'India', 'region': 'South Asia',
        'gradient': 'linear-gradient(135deg,#FF9933,#138808)',
        'hero_color': '#FF9933',
        'overview': 'India is the world\'s most populous nation and one of the fastest-growing major economies, with a GDP exceeding USD 3.5 trillion. Its dynamic business environment — spanning manufacturing, technology, pharmaceuticals, financial services, and agriculture — presents extraordinary opportunities for both domestic and international investors. The Indian regulatory landscape has undergone transformational reform over the past decade, with GST unifying indirect taxation, the Insolvency and Bankruptcy Code streamlining resolution processes, and SEBI strengthening capital market oversight.',
        'key_services': ['GST Registration & Compliance', 'Income Tax Filing & Advisory', 'Transfer Pricing Documentation', 'Company Incorporation (Pvt Ltd / LLP)', 'FEMA & RBI Compliance', 'SEBI & MCA Regulatory Filings', 'Provident Fund (PF) & ESI Compliance', 'Statutory Audit (Ind AS / IGAAP)'],
        'regulators': [('CBDT', 'Central Board of Direct Taxes — income tax administration'), ('GSTN', 'GST Network — indirect tax compliance portal'), ('SEBI', 'Securities and Exchange Board of India'), ('MCA', 'Ministry of Corporate Affairs — company law'), ('RBI', 'Reserve Bank of India — FEMA & forex'), ('IBBI', 'Insolvency & Bankruptcy Board')],
        'investment': 'India offers a liberalised FDI regime under the automatic route for most sectors. The Production-Linked Incentive (PLI) scheme, dedicated economic zones, and strategic infrastructure investments make India a priority destination. Archway advises on FEMA compliance, entry structure selection (wholly owned subsidiary, joint venture, branch, liaison office), and ongoing regulatory obligations.',
        'blog_slug': 'india-digital-tax-revolution-2025',
        'blog_label': 'Read Our India Insight',
    },
    'australia': {
        'name': 'Australia', 'region': 'Asia-Pacific',
        'gradient': 'linear-gradient(135deg,#003087,#CF142B)',
        'hero_color': '#003087',
        'overview': 'Australia ranks among the world\'s most stable and transparent economies, consistently placed in the top tier for ease of doing business, rule of law, and institutional quality. With deep capital markets, a sophisticated financial services sector, and strong trade links across Asia-Pacific, Australia serves as both a prime investment destination and a regional headquartering hub. Recent regulatory developments — mandatory climate disclosures, enhanced ASIC enforcement, and the Foreign Investment Review Board (FIRB) framework — require expert guidance for international businesses.',
        'key_services': ['ATO Tax Compliance & Filing', 'GST Registration & BAS Lodgement', 'Company Registration (ASIC)', 'FIRB Application & Advisory', 'Superannuation (Super) Compliance', 'Climate & ESG Disclosure Advisory', 'Corporate Governance (ASX Listing Rules)', 'Transfer Pricing & Thin Capitalisation'],
        'regulators': [('ATO', 'Australian Taxation Office — federal tax'), ('ASIC', 'Australian Securities & Investments Commission'), ('FIRB', 'Foreign Investment Review Board'), ('APRA', 'Australian Prudential Regulation Authority'), ('ACCC', 'Australian Competition & Consumer Commission'), ('ASX', 'Australian Securities Exchange')],
        'investment': 'Australia welcomes foreign investment across most sectors under the FIRB framework. Key considerations include FIRB notification thresholds, thin capitalisation rules for debt-funded structures, and the R&D tax incentive scheme. Archway guides businesses through the FIRB application process, optimal entity structuring (Pty Ltd, branch, trust), and ongoing ATO compliance.',
        'blog_slug': 'australia-corporate-governance-2025',
        'blog_label': 'Read Our Australia Insight',
    },
    'united-states': {
        'name': 'United States', 'region': 'North America',
        'gradient': 'linear-gradient(135deg,#3C3B6E,#B22234)',
        'hero_color': '#3C3B6E',
        'overview': 'The United States remains the world\'s largest economy by nominal GDP and the foremost destination for international investment. Its vast consumer market, deep capital pools, advanced technology ecosystem, and strong legal institutions make it indispensable for any global growth strategy. Navigating the United States tax environment — federal, state, and local — demands specialist expertise, particularly for cross-border structures subject to GILTI, FDII, BEAT, and Pillar Two rules.',
        'key_services': ['Federal & State Income Tax Compliance', 'US GAAP Financial Reporting', 'Transfer Pricing Documentation (IRC §482)', 'GILTI / FDII / BEAT Analysis', 'Delaware / Nevada Incorporation', 'IRS Voluntary Disclosure Programs', 'M&A Advisory & Due Diligence', 'AI-enabled Finance Function Transformation'],
        'regulators': [('IRS', 'Internal Revenue Service — federal taxation'), ('SEC', 'Securities and Exchange Commission'), ('FINRA', 'Financial Industry Regulatory Authority'), ('FASB', 'Financial Accounting Standards Board'), ('PCAOB', 'Public Company Accounting Oversight Board'), ('OFAC', 'Office of Foreign Assets Control')],
        'investment': 'The United States operates under a federal system with no single national FDI screening authority for most investments, though CFIUS reviews transactions involving national security considerations. State-level incentives, opportunity zones, and research tax credits (Section 41) provide significant investment benefits. Archway advises on optimal entry structures — C-Corp, LLC, partnership — and ongoing multi-state compliance.',
        'blog_slug': 'usa-ai-finance-function-2025',
        'blog_label': 'Read Our United States Insight',
    },
    'canada': {
        'name': 'Canada', 'region': 'North America',
        'gradient': 'linear-gradient(135deg,#D80621,#8C0010)',
        'hero_color': '#D80621',
        'overview': 'Canada combines political stability, abundant natural resources, and a highly educated workforce with deep integration into the North American economy through CUSMA (formerly NAFTA). Its institutional investor base — CPPIB, OTPP, OMERS, and others — is among the world\'s most sophisticated, making Canada a critical partner for cross-border deal activity. The Canada-India bilateral relationship has grown significantly, with increasing trade flows and a large and influential Indian diaspora community.',
        'key_services': ['CRA Corporate Tax Compliance', 'GST/HST Registration & Filing', 'Investment Canada Act Review', 'Transfer Pricing (CRA Guidelines)', 'Canada Business Corporations Act Filings', 'SR&ED Tax Credit Advisory', 'Cross-Border M&A & Due Diligence', 'RRSP / Pension Plan Compliance'],
        'regulators': [('CRA', 'Canada Revenue Agency — federal taxation'), ('OSC', 'Ontario Securities Commission'), ('OSFI', 'Office of the Superintendent of Financial Institutions'), ('Innovation Canada', 'Investment Canada Act reviews'), ('FINTRAC', 'Financial Transactions & Reports Analysis Centre'), ('TSX', 'Toronto Stock Exchange')],
        'investment': 'Canada\'s Investment Canada Act requires notification and in some cases review of foreign acquisitions above defined thresholds. Canada offers generous R&D incentives through the SR&ED program and provincial investment credits. Archway guides businesses through ICA submissions, optimal corporate structure selection (federal vs. provincial incorporation), and CRA compliance for Canadian operations.',
        'blog_slug': 'canada-india-cross-border-ma-opportunities',
        'blog_label': 'Read Our Canada Insight',
    },
    'new-zealand': {
        'name': 'New Zealand', 'region': 'Asia-Pacific',
        'gradient': 'linear-gradient(135deg,#00247D,#CF142B)',
        'hero_color': '#00247D',
        'overview': 'New Zealand consistently ranks first or second globally for ease of doing business, transparency, and absence of corruption. Its stable legal system (based on English common law), extensive double tax agreement network, and Asia-Pacific time-zone positioning make it a favoured regional headquarters and holding company jurisdiction. The New Zealand government has been proactive in developing a modern regulatory framework for digital services, financial technology, and climate reporting.',
        'key_services': ['IRD Income Tax & GST Compliance', 'Companies Office Registration', 'FMCA Financial Services Compliance', 'AML/CFT Programme Design', 'Tax Treaty Planning & Structuring', 'Look-Through Company (LTC) Advisory', 'NZ-Australia Trans-Tasman Structuring', 'Climate-Related Disclosures (XRB)'],
        'regulators': [('IRD', 'Inland Revenue Department — taxation'), ('Companies Office', 'Company registration & filings'), ('FMA', 'Financial Markets Authority'), ('RBNZ', 'Reserve Bank of New Zealand'), ('XRB', 'External Reporting Board — standards'), ('Commerce Commission', 'Competition & consumer law')],
        'investment': 'New Zealand has no general foreign investment review regime for most sectors, making it highly accessible. The Overseas Investment Act applies to sensitive land and significant business assets. New Zealand\'s extensive DTA network (including with India, Australia, UK, US, and China) provides effective tax planning opportunities. Archway assists with entity structuring, IRD registration, and ongoing compliance.',
        'blog_slug': 'new-zealand-apac-headquarters-strategy',
        'blog_label': 'Read Our New Zealand Insight',
    },
    'south-africa': {
        'name': 'South Africa', 'region': 'Sub-Saharan Africa',
        'gradient': 'linear-gradient(135deg,#007A4D,#002395)',
        'hero_color': '#007A4D',
        'overview': 'South Africa is the most industrialised economy on the African continent and the gateway to sub-Saharan Africa\'s 1.2 billion consumers. Its world-class financial services sector, Johannesburg Stock Exchange (the largest in Africa), sophisticated legal system, and established professional services infrastructure make it the natural base for pan-African operations. The B-BBEE framework is a defining feature of the South African business environment and requires specialist advisory to navigate effectively.',
        'key_services': ['SARS Income Tax & VAT Compliance', 'B-BBEE Verification & Strategy', 'Companies Act (CIPC) Filings', 'JSE Listing Requirements Advisory', 'Exchange Control (SARB) Compliance', 'Transfer Pricing (SARS Guidelines)', 'Cross-Border Investment Structuring', 'Africa Gateway Entry Strategy'],
        'regulators': [('SARS', 'South African Revenue Service — taxation'), ('CIPC', 'Companies and Intellectual Property Commission'), ('JSE', 'Johannesburg Stock Exchange'), ('SARB', 'South African Reserve Bank — forex'), ('FSCA', 'Financial Sector Conduct Authority'), ('Competition Commission', 'Merger & competition review')],
        'investment': 'South Africa welcomes foreign investment with no general prior approval regime, though strategic sectors are subject to equity restrictions. Exchange control regulations administered by SARB govern the movement of capital. B-BBEE compliance is critical for businesses operating in South Africa — affecting licensing, government contracts, and supply chain relationships. Archway advises on B-BBEE strategy, investment structuring, and SARS obligations.',
        'blog_slug': 'south-africa-foreign-investment-bbbee-guide',
        'blog_label': 'Read Our South Africa Insight',
    },
    'united-kingdom': {
        'name': 'United Kingdom', 'region': 'Europe',
        'gradient': 'linear-gradient(135deg,#012169,#C8102E)',
        'hero_color': '#012169',
        'overview': 'The United Kingdom remains one of the world\'s leading financial centres and a premier destination for international investment. London\'s position as a global hub for finance, professional services, technology, and creative industries — combined with the UK\'s extensive double tax treaty network and world-class common law legal system — makes it an essential market for any globally-oriented business. Post-Brexit, the UK has developed an independent regulatory framework across financial services, trade, and data protection, creating both new complexities and new opportunities for businesses operating between the UK and international markets.',
        'key_services': ['HMRC Corporation Tax Compliance', 'VAT Registration & Returns', 'Companies House Annual Filings', 'FCA Regulatory Advisory', 'Transfer Pricing (OECD Guidelines)', 'R&D Tax Credits (RDEC & SME Scheme)', 'Post-Brexit Trade & Customs Compliance', 'Cross-Border M&A Advisory'],
        'regulators': [('HMRC', 'HM Revenue & Customs — taxation authority'), ('FCA', 'Financial Conduct Authority — financial services'), ('Companies House', 'Company registration & annual filings'), ('PRA', 'Prudential Regulation Authority — banking & insurance'), ('CMA', 'Competition & Markets Authority — merger review'), ('FRC', 'Financial Reporting Council — accounting standards')],
        'investment': 'The UK operates a largely open investment environment, though the National Security and Investment Act 2021 introduced mandatory notification requirements for acquisitions in 17 sensitive sectors including AI, defence, energy, and telecoms. The UK\'s double tax treaty network — one of the world\'s largest with over 130 agreements — provides effective planning opportunities. Archway advises on optimal entry structures (UK Ltd, LLP, branch), HMRC registration, Making Tax Digital compliance, and ongoing regulatory obligations.',
        'blog_slug': 'uk-post-brexit-trade-advisory-2025',
        'blog_label': 'Read Our UK Insight',
    },
}


@app.route('/countries/<slug>')
def country_detail(slug):
    data = COUNTRY_DATA.get(slug)
    if not data:
        return redirect(url_for('countries'))
    return render_template('country_detail.html', country=data, slug=slug)


@app.route('/blog')
def blog():
    blogs = load_blogs()
    country_filter = request.args.get('country', '')
    category_filter = request.args.get('category', '')
    if country_filter:
        blogs = [b for b in blogs if b['country'].lower() == country_filter.lower()]
    if category_filter:
        blogs = [b for b in blogs if b['category'].lower() == category_filter.lower()]
    all_blogs = load_blogs()
    countries  = sorted(set(b['country'] for b in all_blogs))
    categories = sorted(set(b['category'] for b in all_blogs))
    return render_template('blog.html', blogs=blogs,
                           countries=countries, categories=categories,
                           country_filter=country_filter,
                           category_filter=category_filter)


@app.route('/blog/<slug>')
def blog_post(slug):
    blogs = load_blogs()
    post  = next((b for b in blogs if b['slug'] == slug), None)
    if not post:
        return redirect(url_for('blog'))
    others = [b for b in blogs if b['slug'] != slug][:3]
    return render_template('blog_post.html', post=post, related=others)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Collect form data
        name         = request.form.get('name', '').strip()
        email        = request.form.get('email', '').strip()
        company      = request.form.get('company', '').strip()
        phone        = request.form.get('phone', '').strip()
        country      = request.form.get('country', '').strip()
        service      = request.form.get('service', '').strip()
        rfp_type     = request.form.get('rfp_type', 'General Enquiry')
        message_body = request.form.get('message', '').strip()
        is_rfp       = request.form.get('is_rfp') == 'yes'

        subject_prefix = '[RFP Request]' if is_rfp else '[Contact Enquiry]'
        subject = f"{subject_prefix} {name} — {company or email}"

        body = f"""
{'=' * 60}
{'RFP REQUEST' if is_rfp else 'CONTACT ENQUIRY'} — ARCHWAY ECO-FINTECH WEBSITE
{'=' * 60}

Name:    {name}
Email:   {email}
Company: {company}
Phone:   {phone}
Country: {country}
Service: {service}
Type:    {rfp_type}

Message:
{message_body}

{'=' * 60}
Submitted via archway.in on {datetime.now().strftime('%d %B %Y, %H:%M')}
"""
        try:
            msg = Message(subject=subject,
                          recipients=[RECIPIENT_EMAIL],
                          reply_to=email,
                          body=body)
            mail.send(msg)
            flash('success', 'success')
        except Exception as e:
            app.logger.error(f'Mail send error: {e}')
            flash('error', 'error')

        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route('/googled334c34ae49f0334.html')
def google_verification():
    return 'google-site-verification: googled334c34ae49f0334.html'


@app.route('/sitemap.xml')
def sitemap():
    """Generate dynamic XML sitemap"""
    pages = []
    base_url = 'https://www.archwayadvisors.in'

    # Static pages
    static_pages = [
        ('/', '1.0', 'daily'),
        ('/about', '0.8', 'monthly'),
        ('/why-us', '0.8', 'monthly'),
        ('/services', '0.9', 'weekly'),
        ('/countries', '0.9', 'weekly'),
        ('/blog', '0.9', 'daily'),
        ('/contact', '0.7', 'monthly'),
    ]

    for url, priority, changefreq in static_pages:
        pages.append({
            'loc': base_url + url,
            'priority': priority,
            'changefreq': changefreq,
        })

    # Country pages
    for slug in COUNTRY_DATA.keys():
        pages.append({
            'loc': f'{base_url}/countries/{slug}',
            'priority': '0.8',
            'changefreq': 'monthly',
        })

    # Blog posts
    blogs = load_blogs()
    for blog in blogs:
        pages.append({
            'loc': f'{base_url}/blog/{blog["slug"]}',
            'priority': '0.7',
            'changefreq': 'monthly',
        })

    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for page in pages:
        sitemap_xml += '  <url>\n'
        sitemap_xml += f'    <loc>{page["loc"]}</loc>\n'
        sitemap_xml += f'    <priority>{page["priority"]}</priority>\n'
        sitemap_xml += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        sitemap_xml += '  </url>\n'

    sitemap_xml += '</urlset>'

    return Response(sitemap_xml, mimetype='application/xml')


@app.route('/robots.txt')
def robots():
    """Generate robots.txt file"""
    robots_txt = """User-agent: *
Allow: /

Sitemap: https://www.archwayadvisors.in/sitemap.xml
"""
    return Response(robots_txt, mimetype='text/plain')


# ── Run ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5001)
