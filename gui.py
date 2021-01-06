from flask import Flask, render_template, request, redirect, jsonify
import os, subprocess, threading

class Progress(threading.Thread):
    def __init__(self, root, file_max_length):
        self.progress = 0
        self.all_files = []
        self.root = root
        self.file_max_length = file_max_length
        super().__init__()

    def run(self):
        all_files = []

        # imp = impact => how many percent to add on the progress bar
        imp = 0

        root_subpaths = [f.path for f in os.scandir(self.root) if f.is_dir()]
        # os.walk over the root to get all paths possible
        for path, subdirs, files in os.walk(self.root):
            if imp == 0:
                imp = 100/len(subdirs)
            if imp != 0 and path in [f for f in root_subpaths]:
                self.progress += imp
            for name in files:
                # if path is longer than file_max_length, store it in all_files
                if len(os.path.join(path, name)) > self.file_max_length:
                    all_files.append({"path": path, "name": name, "length": len(os.path.join(path, name))})

        self.all_files = all_files
        self.sort()

    def sort(self):
        # sort all paths by length and reverse it so that the longest is at the top
        self.all_files = sorted(self.all_files, key=lambda k: k['length'])
        self.all_files.reverse()


app = Flask(__name__)
root = r"C:\Users\Admin\Documents\coding\Private\testAzure"
file_max_length = 10
progress = Progress(root, file_max_length)
pagination_index = 1


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        global progress
        progress = Progress(root, file_max_length)
        progress.start()
        #os.system(r"net use P: \\srilch4\Projekte ilchmI04 /user:administrator")
        return render_template('progress.html')
    else:
        return redirect('/files')

@app.route("/files")
def files():
    global progress, pagination_index
    all_files = []
    min_file_index = 20*(pagination_index-1)
    if min_file_index < 0: min_file_index = 0
    max_file_index = 20*pagination_index
    is_max = False
    for i in range(min_file_index, max_file_index):
        if len(progress.all_files) > i:
            all_files.append(progress.all_files[i])
        else:
            is_max = True
    return render_template('files.html', data=all_files, pi=pagination_index, is_max=is_max, max=int(len(progress.all_files)/20+1))


@app.route("/paginate", methods=["POST"])
def paginate():
    global pagination_index
    pagination_index = int(request.form["page_index"])
    return redirect("/files")


@app.route("/rename/get_new_name", methods=["POST"])
def rename_file():
    path = request.form["path"]
    file = request.form["name"]
    name, _ = os.path.splitext(file)
    return render_template("/rename_path.html", path=path, file=file, name=name)

@app.route("/rename", methods=["POST"])
def rename():
    # get process ==> all paths sit there
    global progress

    original_file = request.form["original_name"]
    original_path = request.form["original_path"]
    original_full_path = os.path.join(original_path, original_file)
    _, original_extension = os.path.splitext(original_file)
    new_name = request.form["new_name"]

    # rename file in actual filesystem
    os.rename(original_full_path, os.path.join(original_path, new_name + original_extension))

    # interate over all files in process, then rename the correct file in process
    # this is just for performance (similar to cache), all paths are stored and modified in the process object
    for i in range(len(progress.all_files)):
        path_from_progress = os.path.join(progress.all_files[i]['path'], progress.all_files[i]['name'])
        if original_full_path in path_from_progress:
            progress.all_files[i]['name'] = new_name + original_extension
            progress.all_files[i]['length'] = len(os.path.join(original_path, new_name + original_extension))

    progress.sort()
    return redirect("/files")

@app.route("/open_explorer", methods=["POST"])
def open_explorer():
    subprocess.Popen(r'explorer /select,'+os.path.join(request.form["path"], request.form["name"]))
    return redirect("/files")

@app.route("/progress")
def update_progress():
    global progress
    return jsonify(progress=progress.progress)

if __name__ == "__main__":
    app.run(debug=True)
