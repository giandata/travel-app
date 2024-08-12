import pdfkit
from io import BytesIO


def create_pdf(title_and_summary, days, overall_summary):
    """
    Create a PDF that includes multiple text parts in a specified order using pdfkit.

    :param title_and_summary: Combined title and summary to include in the PDF
    :param days: List of days to include in the PDF
    :param overall_summary: Overall summary to include in the PDF
    :return: BytesIO buffer containing the generated PDF
    """
    config = pdfkit.configuration(
        wkhtmltopdf="C:/Users/39380/Desktop/workspace/projects/travel-app/wkhtmltopdf/bin/wkhtmltopdf.exe"
    )
    # Create the HTML content
    days_list = "".join([f"<li>{day}</li>" for day in days])
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            h1 {{
                font-size: 24px;
                color: #333;
            }}
            h2 {{
                font-size: 20px;
                color: #555;
            }}
            p {{
                font-size: 16px;
                color: #444;
            }}
            ul {{
                font-size: 16px;
                color: #444;
            }}
        </style>
    </head>
    <body>
        <h1>{title_and_summary}</h1>
        <h2>Days:</h2>
        <ul>
            {days_list}
        </ul>
        <h2>Overall Summary:</h2>
        <p>{overall_summary}</p>
    </body>
    </html>
    """

    # Generate PDF from HTML string
    pdf_buffer = BytesIO()
    pdf_buffer.write(pdfkit.from_string(html_content, False, configuration=config))

    # Move the buffer's pointer to the beginning
    pdf_buffer.seek(0)

    return pdf_buffer
