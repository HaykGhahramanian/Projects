import os


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower()


def save_file(file, course_name, topic_subtopic, sec_filename, root_path):
    file_name_from_request = file.filename
    if allowed_file(file_name_from_request):
        filename_for_save = f'{course_name}_{topic_subtopic}_{sec_filename}'
        folder_path = os.path.join(root_path, course_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, filename_for_save)
        file.save(file_path)
        return file_path
    return
