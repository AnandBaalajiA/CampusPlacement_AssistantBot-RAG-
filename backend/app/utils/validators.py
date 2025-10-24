"""
Input validation utilities
"""
def allowed_file(filename, allowed_extensions):
    """Check if file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def validate_query(query):
    """Validate user query"""
    if not query or not isinstance(query, str):
        return False, "Query must be a non-empty string"
    
    if len(query.strip()) < 3:
        return False, "Query is too short"
    
    if len(query) > 1000:
        return False, "Query is too long (max 1000 characters)"
    
    return True, None
