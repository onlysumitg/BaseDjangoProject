from django.core.management.base import BaseCommand, CommandError
import os

from pathlib import Path

class Command(BaseCommand):
    help = 'Rename BaseDjangoProject to your new project'

    excluded_files = ['rename_project.py','db.sqlite3','.txt','.md', 'Pipfile','.lock','.pyc','.css','.gz','.woff','.png','.js','.jpg',
                      '.map'
                      ]
    excluded_folders = ['.git','.idea','__pycache__','coreui','static']

    def add_arguments(self, parser):
        parser.add_argument('new_project_name',   type=str)
        parser.add_argument('old_project_name',   type=str , nargs='?', default='BaseDjangoProject')
        parser.add_argument(
            '--commit',
            action='store_true',
            help='Commit the rename in files',
        )

    def handle(self, *args, **options):
        new_project_name = options.get('new_project_name', None)
        old_project_name = options.get('old_project_name', 'BaseDjangoProject')
        if not new_project_name:
            raise CommandError('Parameter new_project_name required.')

        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        self.stdout.write(self.style.SUCCESS(f"renaming project from {old_project_name} to {new_project_name} {BASE_DIR}"))
        for folderName, subFolders,    fileNames in os.walk(BASE_DIR):
            #self.stdout.write(f'{folderName} ::  {subFolders}  :: {fileNames}')

            if any(ext in folderName for ext in self.excluded_folders):
                continue

            if folderName.strip() == old_project_name:
                self.stdout.write(self.style.WARNING(f"Need to rename folder {folderName}"))

            for subfolder in subFolders:
                if subfolder.strip() == old_project_name:
                    self.stdout.write(self.style.WARNING(f"Need to rename folder {folderName} /{subfolder}"))

            for filename in fileNames:

                full_path = os.path.join(folderName,filename)

                if filename.strip() == old_project_name:
                    self.stdout.write(self.style.WARNING(f"Need to rename file {folderName} /{filename}"))

                is_excluded=  any(filename.endswith(ext) for ext in self.excluded_files)
                if not is_excluded and self.has_old_project_name(full_path,old_project_name):
                    self.stdout.write(self.style.SUCCESS(f"updating file {full_path}"))
                    if options['commit']:
                        self.rename_project_in_file_content(full_path,old_project_name,new_project_name)


    def has_old_project_name(self, file_name, old_project_name):
        # Read in the file
        with open(file_name, 'r') as file :
                try:
                    for line in file.readlines():
                        if old_project_name in line:
                            return True
                except Exception as e:
                    pass


    def rename_project_in_file_content(self, file_name, old_project_name,new_project_name):
        print(">>>>>>>>>>>>>>>>>>>>>> commit>>>>>>>>>>")
        # Read in the file
        with open(file_name, 'r') as file :
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace(old_project_name, new_project_name)

        # Write the file out again
        with open(file_name, 'w') as file:
            file.write(filedata)