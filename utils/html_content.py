def get_invitation_html(semester, course_name, course_code, branch, deadline, link):
    html_content = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Accept/Reject Buttons</title>
<style>
    body {{
        font-family: Arial, sans-serif;
        text-align: center;
        background-color: #f0f0f0;
        margin: 0;
        padding: 20px;
    }}
    .container {{
        max-width: 600px;
        margin: 20px auto;
        padding: 20px;
        background-color: #fff;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        border: 2px solid black;

    }}
    p {{
        margin-bottom: 10px;
    }}
    .btn {{
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        text-decoration: none;
        border: 1px solid #333;
        background-color: #333;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }}
    .accept-btn:active {{
        background-color: #165d1a;
    }}
    .reject-btn:active {{
        background-color: rgb(93, 13, 13);
    }}
    .accept-btn {{
        background-color: green;
        color: white;
        margin-bottom: 5px;

    }}
    .reject-btn {{
        background-color: red;
        color: white;
    }}
</style>
</head>
<body>
    <div class="container">
        <p><strong>College:</strong> XYZ</p>
        <p><strong>Semester:</strong> {semester}</p>
        <p><strong>Course Name:</strong> {course_name}</p>
        <p><strong>Course Code:</strong> {course_code}</p>
        <p><strong>Branch:</strong> {branch}</p>
        <p><strong>Deadline:</strong> {deadline}</p>

        <div>
            <a href={link+'1'}><button class="btn accept-btn" >Accept</button></a>
            <a href={link+'0'}><button class="btn reject-btn">Reject</button></a>
        </div>
    </div>
</body>
</html>
"""
    return html_content


def get_qp_details_html(name, semester, course_name, course_code, branch, deadline, syllabus_copy_link, upload_link):
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Acceptance Confirmation</title>
<style>
    body {{
        font-family: Arial, sans-serif;
        text-align: center;s
        background-color: #f0f0f0;
        margin: 0;
        padding: 20px;
    }}
    .container {{
        max-width: 600px;
        margin: 20px auto;
        padding: 20px;
        background-color: #fff;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        border: 2px solid #333;
    }}
    h3 {{
        margin-bottom: 20px;
        color: green;
    }}
    .tick_container {{
        width: 65px;
        height: 65px;
        background-color: green;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto 20px auto;
    }}
    .tick {{
        font-size: 50px;
        color: white;
    }}
    p {{
        margin-bottom: 15px;
    }}
    .footer {{
        margin-top: 30px;
        font-size: 14px;
        color: #777;
    }}
    .btn {{
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        text-decoration: none;
        border: 1px solid #333;
        background-color: green;
        border-radius: 5px;
        margin-bottom: 10px;
        transition: background-color 0.3s ease;
        color:white;
    }}
</style>
</head>
<body>
    <div class="container">
        <h3>ACCEPTANCE CONFIRMATION</h3>
        <div class="tick_container">
            <div class="tick">&#10004;</div>
        </div>
        <p>Dear {name},</p>
        <p>Thanks for accepting the invitation to set the question paper. Please find attached, the repuired documents.</p>

        <p><strong>College:</strong> XYZ</p>
        <p><strong>Semester:</strong> {semester}</p>
        <p><strong>Course Name:</strong> {course_name}</p>
        <p><strong>Course Code:</strong> {course_code}</p>
        <p><strong>Branch:</strong> {branch}</p>
        <p><strong>Deadline:</strong> {deadline}</p>
        <div>
            <a href='{syllabus_copy_link}'><button class="btn ">SYLLABUS URL</button></a>
            <a href='{upload_link}'><button class="btn " ><i class="fas fa-arrow-up"></i>UPLOAD QP</button></a>
        </div>
        <div class="footer">
            <p>This is an automated email. Please do not reply.</p>
        </div>
    </div>

</body>
</html>

"""
    return html_content
