commands = {
    "install_libraries"  : ["--install_libraries", "-il"],
    "verify_libraries"   : ["--verify_libraries" , "-vl"],

    "new_project"        : ["--new_project"      , "-new", "-n"],
    "make_controller"    : ["--make_controller"  , "-co"],
    "make_manager_controller" : ["--make_manager_controller"  , "-mco"],
    "make_database"      : ["--make_database"       , "-da"],
    "make_request"       : ["--make_request"        , "-re"],
    #"make_request"       : ["--make_request"     , "-re"],
    #"run"                : ["--run"              , "-r" ],

    "help"               : ["--help"             , "-h" ],
    #"force_run"          : ["--force_run"        , "-fr"],
    #"migrate"            : ["--migrate"          , "-m" ],
    
}

full_commands = {
    "verify_libraries" : "--verify_libraries",
    "install_libraries": "--install_libraries",

    "new_project"      : "--new_project {project name}",
    "make_controller"  : "--make_controller {controller_name}",
    "make_manager_controller"  : "--make_manager_controller {controller_name}",
    "make_database"    : "--make_database {database_name}",
    "make_request"       : "--make_request {request_name}",

    "help"             : "--help",
    
}