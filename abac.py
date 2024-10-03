def check_access(attributes):
    # Define required attributes and threshold
    required_attributes = ["doctor", "cardiology"]
    threshold = 2

    # Check how many required attributes the user has
    matched_attributes = [attr for attr in attributes if attr in required_attributes]

    # Allow access if the threshold is met
    return len(matched_attributes) >= threshold
