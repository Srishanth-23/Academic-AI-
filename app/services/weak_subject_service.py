def detect_weak_subjects(subjects):
    
    weak_subjects = []

    for subject in subjects:

        name = subject["name"]
        marks = subject["marks"]
        attendance = subject["attendance"]

        if marks < 50 or attendance < 65:

            weak_subjects.append(name)

    return {
        "weak_subjects": weak_subjects
    }