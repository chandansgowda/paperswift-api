def get_invitation_html(link):
    return f"<html><head></head><body><p>Hello,</p>You have been invited to set question paper. Awaiting your response: 1.<a href = {link+'1'}>Accept</a> 2.<a href = {link+'0'}>Reject</a></p></body></html>"

def get_qp_details_html(syllabus_copy_link, upload_link):
    return f"<html><head></head><body><p>Hello,</p>YThanks for accepting the invitation to set the question paper. Please find attached the required format. Use this link to upload the question paper once set - LINK</p></body></html>"