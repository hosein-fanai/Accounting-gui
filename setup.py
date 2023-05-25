import cx_Freeze
import os


os.environ["TCL_LIBRARY"] = r"C:\Users\Hosein\AppData\Local\Programs\Python\Python38\tcl\tcl8.6"
os.environ["TK_LIBRARY"] = r"C:\Users\Hosein\AppData\Local\Programs\Python\Python38\tcl\tk8.6"

cx_Freeze.setup(name="Accounting",
                options={
                    "build_exe":{
                        "packages":["accounting"
                                    ,"frames"
                                    ,"sqlite3"
                                    ,"tkinter"
                                    ,"tkcalendar"
                                    ,"datetime"
                                    ],
                        "include_files":["user.png"
                                        ,"employee.png"
                                        ,"budget.ico"
                                        ,"accounts.db"
                                        ]
                                }
                        },
                description="Test deploy",
                executables=[cx_Freeze.Executable("app.py")]
                )
