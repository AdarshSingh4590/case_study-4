"""
Script to generate self-contained, print-optimized HTML documents for:
1. simple_segmentation.py -> simple_segmentation.html
2. Ecommerce_Customer_Segmentation.ipynb -> Ecommerce_Customer_Segmentation.html (with print controls)
"""

import os
import base64
import pygments
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

def build_simple_segmentation_html():
    py_path = "simple_segmentation.py"
    with open(py_path, "r", encoding="utf-8") as f:
        code_text = f.read()

    elbow_b64 = get_base64_image("elbow_plot.png")
    pca_tsne_b64 = get_base64_image("pca_tsne_clusters.png")

    formatter = HtmlFormatter(
        style="friendly",
        linenos=True,
        cssclass="source-code",
        lineanchors="line",
        linespans="line"
    )
    highlighted_code = pygments.highlight(code_text, PythonLexer(), formatter)
    pygments_css = formatter.get_style_defs(".source-code")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>simple_segmentation.py - E-Commerce Customer Segmentation</title>
  <style>
    /* Reset & Base Fonts */
    *, *::before, *::after {{
      box-sizing: border-box;
    }}
    
    :root {{
      --bg-color: #f8fafc;
      --card-bg: #ffffff;
      --text-main: #1e293b;
      --text-muted: #64748b;
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --border: #e2e8f0;
      --code-font: "JetBrains Mono", "Cascadia Code", "Fira Code", Consolas, "Courier New", monospace;
      --ui-font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }}

    body {{
      font-family: var(--ui-font);
      background-color: var(--bg-color);
      color: var(--text-main);
      margin: 0;
      padding: 0;
      line-height: 1.5;
      font-size: 14px;
      -webkit-font-smoothing: antialiased;
    }}

    /* Top Floating Action Bar (Screen Only) */
    .action-header {{
      position: sticky;
      top: 0;
      z-index: 1000;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--border);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }}

    .file-badge {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .file-icon {{
      width: 32px;
      height: 32px;
      background: #3b82f6;
      color: white;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      font-size: 14px;
      box-shadow: 0 2px 6px rgba(59, 130, 246, 0.35);
    }}

    .file-info h1 {{
      font-size: 16px;
      font-weight: 700;
      margin: 0;
      color: #0f172a;
    }}

    .file-info span {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    .toolbar-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 16px;
      font-size: 13px;
      font-weight: 600;
      border-radius: 6px;
      border: 1px solid transparent;
      cursor: pointer;
      transition: all 0.2s ease;
      text-decoration: none;
    }}

    .btn-primary {{
      background: #2563eb;
      color: #ffffff;
      box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
    }}
    .btn-primary:hover {{
      background: #1d4ed8;
      box-shadow: 0 4px 8px rgba(37, 99, 235, 0.3);
    }}

    .btn-outline {{
      background: #ffffff;
      color: var(--text-main);
      border-color: var(--border);
    }}
    .btn-outline:hover {{
      background: #f1f5f9;
      border-color: #cbd5e1;
    }}

    /* Main Container */
    .container {{
      max-width: 1080px;
      margin: 24px auto;
      padding: 0 20px;
    }}

    /* Document Title Card */
    .doc-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px 30px;
      margin-bottom: 24px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }}

    .doc-card h2 {{
      margin: 0 0 8px 0;
      font-size: 22px;
      color: #0f172a;
    }}

    .doc-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      color: var(--text-muted);
      font-size: 13px;
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid #f1f5f9;
    }}

    .doc-meta-item {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .badge {{
      display: inline-block;
      padding: 2px 8px;
      background: #e0f2fe;
      color: #0369a1;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    /* Code Container Card */
    .code-card {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
      overflow: hidden;
      margin-bottom: 24px;
    }}

    .card-header {{
      background: #f8fafc;
      padding: 12px 20px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 13px;
      font-weight: 600;
      color: #334155;
    }}

    /* Pygments Custom Styling */
    {pygments_css}

    .source-code {{
      font-family: var(--code-font);
      font-size: 12.5px;
      line-height: 1.6;
      margin: 0;
      padding: 16px 0;
      background: #ffffff !important;
      overflow-x: auto;
    }}

    .source-code table {{
      border-collapse: collapse;
      width: 100%;
    }}

    .source-code td.linenos {{
      width: 44px;
      min-width: 44px;
      padding: 0 12px 0 16px;
      text-align: right;
      color: #94a3b8;
      border-right: 1px solid #f1f5f9;
      user-select: none;
      font-size: 11.5px;
    }}

    .source-code td.code {{
      padding-left: 16px;
      padding-right: 20px;
      white-space: pre-wrap;
      word-break: break-all;
    }}

    .source-code pre {{
      margin: 0;
      font-family: inherit;
    }}

    /* Output & Plots Section */
    .section-title {{
      font-size: 18px;
      font-weight: 700;
      margin: 32px 0 16px;
      color: #0f172a;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .output-box {{
      background: #0f172a;
      color: #f8fafc;
      border-radius: 8px;
      padding: 16px 20px;
      font-family: var(--code-font);
      font-size: 12px;
      line-height: 1.55;
      overflow-x: auto;
      margin-bottom: 24px;
      box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.4);
    }}

    .plots-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 30px;
    }}

    @media (max-width: 768px) {{
      .plots-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .plot-card {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px;
      text-align: center;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
      break-inside: avoid;
      page-break-inside: avoid;
    }}

    .plot-card img {{
      max-width: 100%;
      height: auto;
      border-radius: 6px;
      border: 1px solid #f1f5f9;
    }}

    .plot-title {{
      font-weight: 600;
      font-size: 13px;
      margin-top: 10px;
      color: #334155;
    }}

    .table-container {{
      overflow-x: auto;
      background: white;
      border: 1px solid var(--border);
      border-radius: 8px;
      margin-bottom: 24px;
    }}

    table.styled-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      text-align: left;
    }}

    table.styled-table th {{
      background-color: #f8fafc;
      color: #334155;
      padding: 10px 16px;
      font-weight: 600;
      border-bottom: 1px solid var(--border);
    }}

    table.styled-table td {{
      padding: 10px 16px;
      border-bottom: 1px solid #f1f5f9;
      color: #1e293b;
    }}

    table.styled-table tr:last-child td {{
      border-bottom: none;
    }}

    /* =========================================================================
       PRINT OPTIMIZATIONS
       ========================================================================= */
    @media print {{
      @page {{
        size: A4 portrait;
        margin: 12mm 14mm 14mm 14mm;
      }}

      body {{
        background: #ffffff !important;
        color: #000000 !important;
        font-size: 9.5pt !important;
        line-height: 1.4 !important;
      }}

      /* Hide screen-only UI */
      .action-header, .no-print {{
        display: none !important;
      }}

      .container {{
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
      }}

      .doc-card {{
        border: none !important;
        padding: 0 0 12pt 0 !important;
        margin-bottom: 12pt !important;
        box-shadow: none !important;
        border-bottom: 1.5pt solid #000 !important;
      }}

      .doc-card h2 {{
        font-size: 16pt !important;
      }}

      .code-card {{
        border: 1pt solid #cbd5e1 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        margin-bottom: 14pt !important;
      }}

      .card-header {{
        background: #f1f5f9 !important;
        border-bottom: 1pt solid #cbd5e1 !important;
        padding: 6pt 10pt !important;
        font-size: 9pt !important;
        color: #000 !important;
      }}

      .source-code {{
        font-size: 8.5pt !important;
        line-height: 1.4 !important;
        padding: 8pt 0 !important;
      }}

      .source-code td.linenos {{
        width: 30pt !important;
        padding: 0 6pt 0 8pt !important;
        color: #64748b !important;
        border-right: 1pt solid #cbd5e1 !important;
        font-size: 8pt !important;
      }}

      .source-code td.code {{
        padding: 0 8pt !important;
        white-space: pre-wrap !important;
        word-break: break-all !important;
      }}

      .output-box {{
        background: #f8fafc !important;
        color: #0f172a !important;
        border: 1pt solid #cbd5e1 !important;
        font-size: 8.5pt !important;
        box-shadow: none !important;
        page-break-inside: avoid;
        break-inside: avoid;
      }}

      .plots-grid {{
        display: block !important;
        page-break-before: always;
        break-before: page;
      }}

      .plot-card {{
        border: 1pt solid #cbd5e1 !important;
        box-shadow: none !important;
        margin-bottom: 15pt !important;
        page-break-inside: avoid;
        break-inside: avoid;
      }}

      .plot-card img {{
        max-width: 90% !important;
        border: none !important;
      }}

      .page-break {{
        page-break-before: always;
        break-before: page;
      }}

      .avoid-break {{
        page-break-inside: avoid;
        break-inside: avoid;
      }}
    }}
  </style>
</head>
<body>

  <!-- Floating Screen Action Bar (Hidden on Print) -->
  <header class="action-header no-print">
    <div class="file-badge">
      <div class="file-icon">PY</div>
      <div class="file-info">
        <h1>simple_segmentation.py</h1>
        <span>E-Commerce Customer Segmentation Pipeline &bull; 225 Lines</span>
      </div>
    </div>
    <div class="toolbar-actions">
      <button class="btn btn-outline" onclick="toggleOutputs()">
        <span id="output-toggle-text">📊 Toggle Plots &amp; Output</span>
      </button>
      <button class="btn btn-primary" onclick="window.print()">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="6 9 6 2 18 2 18 9"></polyline>
          <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
          <rect x="6" y="14" width="12" height="8"></rect>
        </svg>
        Print / Save as PDF (Ctrl+P)
      </button>
    </div>
  </header>

  <div class="container">
    
    <!-- Document Header Info Card -->
    <div class="doc-card">
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
          <span class="badge">Unsupervised Machine Learning</span>
          <h2 style="margin-top: 8px;">E-Commerce Customer Segmentation Pipeline</h2>
          <p style="margin: 0; color: #475569; font-size: 13.5px;">
            End-to-End Workflow: Data Preprocessing &bull; RFM Feature Engineering &bull; Log Transformation &bull; StandardScaler &bull; K-Means &bull; DBSCAN &bull; PCA &bull; t-SNE &bull; Marketing Personas
          </p>
        </div>
      </div>
      <div class="doc-meta">
        <div class="doc-meta-item"><strong>Source File:</strong> <code>simple_segmentation.py</code></div>
        <div class="doc-meta-item"><strong>Format:</strong> Print-Ready Clean HTML</div>
        <div class="doc-meta-item"><strong>Total Customers:</strong> 216</div>
        <div class="doc-meta-item"><strong>Completed Orders:</strong> 780</div>
      </div>
    </div>

    <!-- Python Script Code Card -->
    <div class="code-card">
      <div class="card-header">
        <span>Python Source Code (simple_segmentation.py)</span>
        <span style="font-weight: normal; color: var(--text-muted);">225 Lines &bull; UTF-8</span>
      </div>
      <div class="source-code">
        {highlighted_code}
      </div>
    </div>

    <!-- Generated Outputs & Plots (Embedded) -->
    <div id="output-section">
      <div class="section-title">
        <span>📊 Pipeline Execution Outputs &amp; Segmentation Results</span>
      </div>

      <!-- Execution Console Log -->
      <div class="output-box">
<pre style="margin: 0; font-family: inherit;">--- Step 1: Loading and Cleaning Data ---
Total raw orders in file: 818
Cleaned completed orders: 780

--- Step 2: Calculating RFM Features ---
Snapshot Reference Date: 2024-12-25 20:41:17
Total unique customers: 216
   customer_id  Recency  Frequency  Monetary
0            1      139          3   1139.51
1            2      188          3    337.63
2            3      275          5    633.89
3            4      328          3    371.32
4            5     1048          1     77.03

--- Step 3: Scaling Features ---
Features successfully log-transformed and standardized.

--- Step 4: K-Means Clustering ---
Saved Elbow Curve to 'elbow_plot.png'. (Optimal K = 4)

--- Step 5: DBSCAN Clustering ---
DBSCAN clusters found: 4
DBSCAN noise points (-1): 22 (10.2%)

--- Step 6: PCA Dimensionality Reduction ---
PCA Explained Variance Ratio: [0.656 0.273] (Cumulative: 92.9%)

--- Step 7: t-SNE Visualization ---
Saved PCA &amp; t-SNE side-by-side plot to 'pca_tsne_clusters.png'.

--- Step 8: Cluster Profiling &amp; Actionable Personas ---
[SUCCESS] Saved customer-level results to 'customer_segments.csv'.
All steps completed successfully!</pre>
      </div>

      <!-- Cluster Profiles Table -->
      <div class="table-container avoid-break">
        <table class="styled-table">
          <thead>
            <tr>
              <th>Cluster ID</th>
              <th>Assigned Marketing Persona</th>
              <th>Avg Recency (Days)</th>
              <th>Avg Frequency (Orders)</th>
              <th>Avg Spend ($)</th>
              <th>Customer Count</th>
              <th>Strategic Marketing Action</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Cluster 3</strong></td>
              <td><span style="color:#16a34a; font-weight:700;">Champions (VIPs)</span></td>
              <td>51.9 days</td>
              <td>6.94 orders</td>
              <td>$519.94</td>
              <td>16 (7.4%)</td>
              <td>VIP loyalty perks, early access, exclusive rewards</td>
            </tr>
            <tr>
              <td><strong>Cluster 2</strong></td>
              <td><span style="color:#d97706; font-weight:700;">At-Risk High-Spenders</span></td>
              <td>421.8 days</td>
              <td>6.63 orders</td>
              <td>$412.09</td>
              <td>75 (34.7%)</td>
              <td>Urgent win-back discounts, personalized re-engagement</td>
            </tr>
            <tr>
              <td><strong>Cluster 1</strong></td>
              <td><span style="color:#2563eb; font-weight:700;">Recent Occasional Buyers</span></td>
              <td>225.9 days</td>
              <td>1.40 orders</td>
              <td>$45.39</td>
              <td>48 (22.2%)</td>
              <td>Nurture campaigns, cross-sell related categories</td>
            </tr>
            <tr>
              <td><strong>Cluster 0</strong></td>
              <td><span style="color:#dc2626; font-weight:700;">Hibernating Customers</span></td>
              <td>665.3 days</td>
              <td>1.36 orders</td>
              <td>$47.53</td>
              <td>77 (35.6%)</td>
              <td>Low-cost email clearance offers; limit paid ads</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Side by Side Visualizations -->
      <div class="plots-grid">
        <div class="plot-card">
          <img src="data:image/png;base64,{elbow_b64}" alt="Elbow Method Curve">
          <div class="plot-title">Figure 1: K-Means Elbow Curve (Selecting K=4)</div>
        </div>
        <div class="plot-card">
          <img src="data:image/png;base64,{pca_tsne_b64}" alt="PCA and t-SNE Projections">
          <div class="plot-title">Figure 2: 2D Dimensionality Reduction (PCA vs. t-SNE)</div>
        </div>
      </div>

    </div>

  </div>

  <script>
    function toggleOutputs() {{
      const sec = document.getElementById('output-section');
      const text = document.getElementById('output-toggle-text');
      if (sec.style.display === 'none') {{
        sec.style.display = 'block';
        text.innerHTML = '📊 Hide Plots &amp; Output';
      }} else {{
        sec.style.display = 'none';
        text.innerHTML = '📊 Show Plots &amp; Output';
      }}
    }}
  </script>
</body>
</html>
"""

    out_file = "simple_segmentation.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Successfully generated {out_file} ({len(html_content)} bytes)")


def enhance_notebook_html():
    nb_html = "Ecommerce_Customer_Segmentation.html"
    if not os.path.exists(nb_html):
        print("Ecommerce_Customer_Segmentation.html does not exist.")
        return

    with open(nb_html, "r", encoding="utf-8") as f:
        content = f.read()

    # Add print-friendly floating toolbar and print styles if not already present
    custom_toolbar = """
    <!-- Antigravity Print Bar -->
    <div id="nb-print-toolbar" style="
      position: sticky;
      top: 0;
      z-index: 99999;
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(8px);
      border-bottom: 2px solid #2563eb;
      padding: 10px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 4px 10px rgba(0,0,0,0.06);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    ">
      <div style="display: flex; align-items: center; gap: 10px;">
        <span style="background: #2563eb; color: #fff; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px;">NOTEBOOK</span>
        <strong style="color: #0f172a; font-size: 15px;">Ecommerce_Customer_Segmentation.ipynb</strong>
      </div>
      <div>
        <button onclick="window.print()" style="
          background: #2563eb;
          color: white;
          border: none;
          padding: 8px 18px;
          border-radius: 6px;
          font-weight: 600;
          font-size: 13px;
          cursor: pointer;
          display: inline-flex;
          align-items: center;
          gap: 6px;
          box-shadow: 0 2px 4px rgba(37,99,235,0.25);
        ">
          🖨️ Print / Save as PDF (Ctrl+P)
        </button>
      </div>
    </div>
    <style>
      @media print {
        #nb-print-toolbar { display: none !important; }
        @page { margin: 12mm; size: A4 portrait; }
        body { font-size: 10pt !important; }
        .jp-Cell { page-break-inside: avoid; break-inside: avoid; }
        pre, code { white-space: pre-wrap !important; word-break: break-all !important; }
      }
    </style>
    """

    if "#nb-print-toolbar" not in content:
        # Inject right after <body...>
        import re
        content = re.sub(r'(<body[^>]*>)', r'\1\n' + custom_toolbar, content, count=1)
        with open(nb_html, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully enhanced {nb_html} with print toolbar and print styles!")

if __name__ == "__main__":
    build_simple_segmentation_html()
    enhance_notebook_html()
