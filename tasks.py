from invoke import task, Collection

from metapack_build.tasks.collection import ns, foreach_metapack_subdir, ns_foreach_task_subdir



@task
def git_add(c):
    """Run git commit -a  on all submodules"""
    c.run(f"git submodule foreach 'git add -A'")

ns.add_task(git_add)

@task
def update_files(c):
    """Print the package url for each sub directory"""
    
    for d in foreach_metapack_subdir(c):
        c.run('mp update -f -S')
        
ns.add_task(update_files)

# This is an example task for iterating over all of the sub directoryies
# that have a data package ( directory with metadata.csv ) Th
# foreach_metapack_subdir generator returns pathlib.Path() for each directory
# and changes the current directory into that directory. 
@task
def foreach_package(c):
    """Print the package url for each sub directory"""
    
    for d in foreach_metapack_subdir(c):
        c.run('mp info -p')
        
ns.add_task(foreach_package)

# You can also iterate over all directories that are set up for
# invoke, with a tasks.py file. The ns_foreach_task_subdir returns the 
# Invoke Collection, which holds all of the tasks for the directory. The 
# generator also changes the current working directory each iteration. 
@task
def foreach_tasks(c):
    """Print invoke's configuration by running the config tasks in each subdirectory """
    for sp_ns in ns_foreach_task_subdir(c):
        try:
            sp_ns.tasks.config(c)
        except UnexpectedExit:
            pass
            
ns.add_task(foreach_tasks)

