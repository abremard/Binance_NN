import logging

def task_start(task_name, verbosity):
    logging.debug(task_name+' - starting job ...')
    logging.debug(f'-------------------------------------------------------------------------------------')
    if verbosity is not 'NONE' :
        print(task_name+' - starting job ...')
        print('-------------------------------------------------------------------------------------')

def task_fail(task_name, verbosity, e):
    logging.debug(f'-------------------------------------------------------------------------------------')
    logging.error("FORMAT INPUT - exception occurred!", exc_info=True)
    if verbosity is not 'NONE' :
        print('-------------------------------------------------------------------------------------')
        print(task_name+' - exception occurred!')
        print(e)
    raise

def task_success(task_name, verbosity):
    logging.debug(f'-------------------------------------------------------------------------------------')
    logging.debug(task_name+' - completed successfully!')
    if verbosity is not 'NONE' :
        print('-------------------------------------------------------------------------------------')
        print(task_name+' - completed successfully!')