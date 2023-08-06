import numpy as np
import pandas as pd
from copy import deepcopy
import time
import sys
import os
import numpy_dataframe as npd
import random
import string


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

class Awk_command:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self):
        super(Awk_command, self).__setattr__('command', "")
        super(Awk_command, self).__setattr__('priority', 3)
        super(Awk_command, self).__setattr__('type', "")
        super(Awk_command, self).__setattr__('persistance_in_time', "continuous")
        super(Awk_command, self).__setattr__('persistance_after_execution', "ephemeral")
        super(Awk_command, self).__setattr__('id', get_random_string(20))
    def __getattr__(self, name):
        return super(Awk_command, self).__getattr__(name)
    def __setattr__(self, name, value):
        super(Awk_command, self).__setattr__(name, value)


class DataFrame:
    def __repr__(self):
        text = self.__head_current__().values()
        shape = self.__shape_current__().values()
        values = shape.replace("\n","").strip().split(",")
        values = np.array(values).astype(int)
        if values[0] > 10:
            text = text + ("...")
        return text
    def __str__(self):
        text = self.__head_current__().values()
        shape = self.__shape_current__().values()
        values = shape.replace("\n","").strip().split(",")
        values = np.array(values).astype(int)
        if values[0] > 10:
            text = text + ("...")
        return text
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self):
        super(DataFrame, self).__setattr__('path', "")
        super(DataFrame, self).__setattr__('commands', [])
        super(DataFrame, self).__setattr__('delimiter', ",")
        super(DataFrame, self).__setattr__('id', get_random_string(20))
        super(DataFrame, self).__setattr__('ncol', 0)
        super(DataFrame, self).__setattr__('nrow', 0)
        super(DataFrame, self).__setattr__('__ncol_original__', 0)
        super(DataFrame, self).__setattr__('__nrow_original__', 0)

    def __getattr__(self, name):
        return super(DataFrame, self).__getattr__(name)

    def __setattr__(self, name, value):
        super(DataFrame, self).__setattr__(name, value)

#         if type(value) == list:
#             value = np.array(value)
#         self.d[name] = value
#         super(DataFrame, self).__setattr__('ncol', self.ncol + 1)
#         if self.nrow == 0:
#             super(DataFrame, self).__setattr__('nrow', len(value))
#     def __getitem__(self,args):
#         if type(args) == tuple:
#             rows,key=args
#             if len(key) == 1:
#                 if type(key) == list:
#                     t_ = DataFrame()
#                     for k in key:
#                         DataFrame.__setattr__(t_,k,self.d[k][rows])
#                     return t_
#                 else:
#                     __ddf__ = deepcopy(self)
# __ddf__.__settle_commands__()
# self.clear_commands()
# return __ddf__.d[key][rows]
#             else:
#                 t_ = DataFrame()
#                 for k in key:
#                     DataFrame.__setattr__(t_,k,self.d[k][rows])
#                 return t_
#         else:
#             key = args
#             if type(key) == str:
#                 __ddf__ = deepcopy(self)
# __ddf__.__settle_commands__()
# self.clear_commands()
# return __ddf__.d[key]
#             else:
#                 if len(key) == 1:
#                     if type(key) == list:
#                         t_ = DataFrame()
#                         for k in key:
#                             DataFrame.__setattr__(t_,k,self.d[k])
#                         return t_
#                     else:
#                         __ddf__ = deepcopy(self)
# __ddf__.__settle_commands__()
# self.clear_commands()
# return __ddf__.d[key]
#                 else:
#                     t_ = DataFrame()
#                     for k in key:
#                         DataFrame.__setattr__(t_,k,self.d[k])
#                     return t_

#     def __setitem__(self,key,values):
#         DataFrame.__setattr__(self,key,values)

    def read_csv(self,path,delimiter = ","):
        self.path = path
        self.delimiter = delimiter

    def shape(self):
        input = self.path
        command = "awk " + """'
        BEGIN {
            FS = \"""" + self.delimiter + """\"
            number_rows = 0
        }
        {
            if (NR == 1){

            }else{
                number_rows+=1

            }
        }
        END {
            printf("%s""" + self.delimiter + """",number_rows)
            print(NF)
        }
        ' """ + input
        result = os.popen(command).read()
        values = result.replace("\n","").strip().split(",")
        values = np.array(values).astype(int)
        ncol = values[1]
        nrow = values[0]
        __ncol_original__ = ncol
        __nrow_original__ = nrow
        return values

    def __shape_current__(self):
        command = "awk " + """'
        BEGIN {
            FS = \"""" + self.delimiter + """\"
            number_rows = 0
        }
        {
            if (NR == 1){

            }else{
                number_rows+=1

            }
        }
        END {
            printf("%s""" + self.delimiter + """",number_rows)
            print(NF)
        }
        ' """
        result = os.popen(command).read()

        awk_command = Awk_command()
        awk_command.command = command
        awk_command.priority = 9999999999
        awk_command.type = "shape"
        awk_command.persistance_in_time = "instance"
        self.commands.append(awk_command)
        return self



    def names(self):
        input = self.path
        command = "awk " + """'
    BEGIN {
        FS = \"""" + self.delimiter + """\"
    }
    {
        if (NR == 1){
            print
            exit
        }
    }
    END {}
    ' """ + input
        result = os.popen(command).read()
        return np.array(result.replace("\n","").split(self.delimiter))

    def __names_current__(self):
        command = "awk " + """'
    BEGIN {
        FS = \"""" + self.delimiter + """\"
    }
    {
        if (NR == 1){
            print
            exit
        }
    }
    END {}
    ' """
        awk_command = Awk_command()
        awk_command.command = command
        awk_command.priority = 9999999999
        awk_command.type = "names"
        awk_command.persistance_in_time = "instance"
        self.commands.append(awk_command)
        return self

    def __to_np_arrays__(self):
        shape = self.shape()
        columns = np.empty(shape[0],list)
        lines = self.values(clear = False).split("\n")
        str_types = self.get_types().values()
        types = []
        types_text = str_types.split(",")
        for type_t  in types_text:
            types.append(eval(type_t))
        line_counter = 0
        names = []
        for line in lines:
            if line != "":
                elements = line.split(self.delimiter)
                if line_counter == 0:
                        names = elements
                else:
                    for i in range(len(elements)):
                        try:
                            columns[i].append(elements[i])
                        except:
                            columns[i] = [elements[i]]

                line_counter += 1
        return names,columns,types

    def to_npd(self):
        names,columns,types = self.__to_np_arrays__()
        t = npd.DataFrame()
        for i in range(len(names)):
            t[names[i]] = np.array(columns[i]).astype(types[i])
        return t

    def to_pandas(self):
        names,columns,types = self.__to_np_arrays__()
        df = pd.DataFrame()
        for i in range(len(names)):
            df[names[i]] = np.array(columns[i]).astype(types[i])
        return df

    def values(self,clear = True):
        complete_command = ""
        record_delimiter = "\\n"
        record_delimiter_transform = "\\n"
        intermediate_record_delimiter = "\\n"
        for command in self.commands:
            if command == self.commands[0]:
                if command != self.commands[len(self.commands)-1]:
                    record_delimiter_transform = "\\n"
                else:
                    record_delimiter_transform = intermediate_record_delimiter
                if command == self.commands[len(self.commands)-1]:
                    record_delimiter_transform = "\\n"
                complete_command = command.command.replace("has_header","1").replace("record_delimiter_transform",record_delimiter_transform).replace("record_delimiter",record_delimiter) + self.path
                record_delimiter = record_delimiter_transform
            else:
                if command != self.commands[len(self.commands)-1]:
                    record_delimiter_transform = intermediate_record_delimiter
                else:
                    record_delimiter_transform = "\\n"
                complete_command = complete_command + " | " + command.command.replace("has_header","1").replace("record_delimiter_transform",record_delimiter_transform).replace("record_delimiter",record_delimiter)
                record_delimiter = record_delimiter_transform
        result = os.popen(complete_command).read()
        new_commands = []
        for command in self.commands:
            if command.persistance_in_time == "continuous":
                new_commands.append(command)
        self.commands = new_commands
        if clear:
            self.clear_commands()
        return result

    def __get_rows_from_to__(self,min_row,max_row,header = True):
        awk_command = Awk_command()
#         if type(rows) == list:
#             rows = np.array(rows)
#         rows_str = np.array2string(rows,separator="\n")
#         rows_str = rows_str[1:len(rows_str)-1]
#         path_rows = os.path.expanduser('~') + "/.tmp/rows_" + self.id + ".txt"
#         command = "echo '" + rows_str + "'>" + path_rows
#         os.system(command)
        variables = "-v header=\"has_header\" -v min_row=\"" + str(min_row) + "\" -v max_row=\"" + str(max_row) + "\" "
        command = "awk " + variables + """'
        BEGIN {
            FS = \"""" + self.delimiter + """\"
            RS = "record_delimiter"
            RS_new = "record_delimiter_transform"

        }
        {
            if (FNR == 1){
                if (header){
                    printf("%s" RS_new,$0)
                }
            }else{
                if (FNR >= min_row + 1 && FNR <= max_row + 1){
                    printf("%s" RS_new,$0)
                }
            }

            if (FNR > max_row + 1){
                exit
            }

        }
        END {

        }
        ' """
        awk_command.command = command
        awk_command.priority = 1
        awk_command.type = "get_rows_range"
        self.commands.append(awk_command)
        __ddf__ = deepcopy(self)
        __ddf__.__settle_commands__()
        self.clear_commands()
        return __ddf__

    def get_rows(self,rows,header = True):
        if type(rows) == range:
            return DataFrame.__get_rows_from_to__(self,min(rows),max(rows))
        else:
            awk_command = Awk_command()
            if type(rows) == list:
                rows = np.array(rows)

            rows_str = np.array2string(rows,separator="\n")
            rows_str = rows_str[1:len(rows_str)-1]
            if not os.path.exists(os.path.expanduser('~') + "/.tmp/"):
                os.mkdir(os.path.expanduser('~') + "/.tmp/")
                print("Creating folder ",os.path.expanduser('~') + "/.tmp/")
            path_rows = os.path.expanduser('~') + "/.tmp/rows_" + self.id + "_" + awk_command.id + ".txt"            
            command = "echo '" + rows_str + "'>" + path_rows
            os.system(command)
            variables = "-v header=\"has_header\" -v min_row=\"" + str(min(rows)) + "\" -v max_row=\"" + str(max(rows)) + "\" -v length_rows=\"" + str(len(rows)) + "\" "
            command = "awk " + variables + """'
            BEGIN {
                FS = \"""" + self.delimiter + """\"
                RS = "record_delimiter"
                RS_new = "record_delimiter_transform"
                rows["1"] = 1
                cmd = "cat """ + path_rows + """\"

                while (cmd | getline) {
                    rows[$0+1] = 1;

                }

                close(cmd)

            }
            {

                if (rows[FNR] == 1){
                    if (FNR == 1){
                        if (header){
                            printf("%s" RS_new,$0)
                        }
                    }else{
                        printf("%s" RS_new,$0)
                    }
                }
                if (FNR > max_row + 1){
                    exit
                }

            }
            END {

            }
            ' """
            awk_command.command = command
            awk_command.priority = 1
            awk_command.type = "get_rows"
            self.commands.append(awk_command)
            __ddf__ = deepcopy(self)
            __ddf__.__settle_commands__()
            self.clear_commands()
            return __ddf__

    def get_cols(self,cols,header = True):
        awk_command = Awk_command()
        if type(cols) == np.array:
            cols = cols.tolist()

        new_cols = np.empty(len(cols),int)

        names = self.names()
        for i in range(len(cols)):
            col = cols[i]
            if type(col) != int:
                index = np.where(names == col)[0]
                new_cols[i] = index
            else:
                new_cols[i] = col
        cols = np.unique(new_cols)

        cols_str = np.array2string(cols,separator="\n")
        cols_str = cols_str[1:len(cols_str)-1]
        if not os.path.exists(os.path.expanduser('~') + "/.tmp/"):
            os.mkdir(os.path.expanduser('~') + "/.tmp/")
            print("Creating folder ",os.path.expanduser('~') + "/.tmp/")
        path_cols = os.path.expanduser('~') + "/.tmp/cols_" + self.id + "_" + awk_command.id + ".txt"
        command = "echo '" + cols_str + "' | sort | xargs -I {} echo \"{}\" >" + path_cols
        os.system(command)
        variables = "-v header=\"has_header\" -v min_col=\"" + str(min(cols)) + "\" -v max_col=\"" + str(max(cols)) + "\" "
        command = "awk " + variables + """'
        BEGIN {
            FS = \"""" + self.delimiter + """\"
            RS = "record_delimiter"
            RS_new = "record_delimiter_transform"
            cmd = "cat """ + path_cols + """\"

            while (cmd | getline) {
                cols[$0+1] = 1;

            }

            close(cmd)
        }
        {

            if (FNR == 1){
                if (header){
                    for (i=min_col+1;i<max_col+1;i++){
                        if (cols[i] == 1){
                            printf("%s""" + self.delimiter + """", $i)
                        }
                    }
                    if (cols[max_col+1] == 1){
                        printf("%s", $(max_col+1))
                    }
                    printf("%s" RS_new,"")
                }
            }else{
                for (i=min_col+1;i<max_col+1;i++){
                    if (cols[i] == 1){
                        printf("%s""" + self.delimiter + """", $i)
                    }
                }
                if (cols[max_col+1] == 1){
                    printf("%s", $(max_col+1))
                }
                printf("%s" RS_new,"")

            }

        }
        END {

        }
        ' """
        awk_command.command = command
        awk_command.priority = 2
        awk_command.type = "get_cols"
        self.commands.append(awk_command)
        __ddf__ = deepcopy(self)
        __ddf__.__settle_commands__()
        self.clear_commands()
        return __ddf__

    def clear_commands(self):
        new_commands = []
        for command in self.commands:
            if command.persistance_after_execution != "ephemeral":
                new_commands.append(command)
            else:
                if command.type == "get_cols":
                    path_cols = os.path.expanduser('~') + "/.tmp/cols_" + self.id + "_" + command.id + ".txt"
                    if os.path.exists(path_cols):
                        os.remove(path_cols)
                if command.type == "get_rows":
                    path_rows = os.path.expanduser('~') + "/.tmp/rows_" + self.id + "_" + command.id + ".txt"
                    if os.path.exists(path_rows):
                        os.remove(path_rows)
                
        self.commands = new_commands
        
    def clear_all_commands(self):
        for command in self.commands:            
            if command.type == "get_cols":
                path_cols = os.path.expanduser('~') + "/.tmp/cols_" + self.id + "_" + command.id + ".txt"
                if os.path.exists(path_cols):
                    os.remove(path_cols)
            if command.type == "get_rows":
                path_rows = os.path.expanduser('~') + "/.tmp/rows_" + self.id + "_" + command.id + ".txt"
                if os.path.exists(path_rows):
                    os.remove(path_rows)
        self.commands = []

    def __settle_commands__(self):
        for command in self.commands:
            command.persistance_after_execution = "permanent"

    def get_types(self,num_rows_to_check = 1000):
        awk_command = Awk_command()
        command = "awk " + """'
        BEGIN {
            FS = \"""" + self.delimiter + """\"
            number_rows = 0
            types[""] = "int"
        }
        {
            if (NR == 1){
                for (i=1;i<=NF;i++){
                    types[$i] = "int"
                }
            }else{

                for (i=1;i<=NF;i++){
                    if ($i ~ /^[0-9]+$/){
                        types[$i] = "int"
                    }else{
                        if ($i ~ /^[0-9]*[.][0-9]+$/){
                            types[$i] = "float"
                        }else{
                            types[$i] = "str"
                        }
                    }
                }
                if (NR > """ + str(num_rows_to_check) + """){
                    exit
                }
            }
        }
        END {
            for (i=1;i<NF;i++){
                printf("%s""" + self.delimiter + """",types[$i])
            }
            printf("%s",types[$NF])
            print("")
        }
        ' """

        awk_command.command = command
        awk_command.priority = 9999999999
        awk_command.type = "get_cols"
        awk_command.persistance_in_time = "instance"
        self.commands.append(awk_command)
        __ddf__ = deepcopy(self)
        __ddf__.__settle_commands__()
        self.clear_commands()
        return __ddf__

    def head(self,n=10):
        awk_command = Awk_command()
        command = "awk " + """'
        BEGIN {
            FS = ","
        }
        {
            if (NR < """ + str(n+2) + """){
                print
            }else{
                exit
            }
        }
        END {}
        ' """ + self.path


#         awk_command.command = command
#         awk_command.priority = 9999999999
#         awk_command.type = "get_cols"
#         awk_command.persistance_in_time = "instance"
#         self.commands.append(awk_command)
#         __ddf__ = deepcopy(self)
# __ddf__.__settle_commands__()
#     self.clear_commands()
# return __ddf__
        result = os.popen(command).read()
        return result

    def __head_current__(self,n=10):
        awk_command = Awk_command()
        command = "awk " + """'
        BEGIN {
            FS = ","
        }
        {
            if (NR < """ + str(n+2) + """){
                print
            }else{
                exit
            }
        }
        END {}
        ' """


        awk_command.command = command
        awk_command.priority = 9999999999
        awk_command.type = "head"
        awk_command.persistance_in_time = "instance"
        self.commands.append(awk_command)
        return self

    def select(self,condition_as_string):

        condition_as_string = condition_as_string.replace(" in ["," _in_ [")

        operators = [">=","<=",">","<","==","!=","~"," ","&&","\|\|","&","\|","!","(",")"]
        text = "echo \"" + condition_as_string + "\" | "
        for operator in operators:
            text = text + "awk 'BEGIN{FS = \"" + operator + "\"}{print($1);for (i=2;i<=NF;i++){if (FS!=\" \"){print (FS)};print($i)}}' | "

        command = text
        command = command + """awk '
        {if ($0 ~ /^[0-9]*[.][0-9]*$/)
            {
                if ($0 ~ /^[.][0-9]*$/){
                    print("0"  $0)
                }else{
                    printf($0)
                    print("")
                }
            }else{print($0)}}
        '"""
        # print(command)
        result = os.popen(command).read()
        result = result.replace("\n\n","\n")
        result = result.replace("\n\n","\n")
        result = result.replace("\n\n","\n")
        result = result.replace("\n\n","\n")
        result = result.replace("\n\n","\n")

        elements = result.split("\n")
        # print(result)
        indices_in = []
        for i in range(len(elements)):
            if elements[i] == "_in_":
                indices_in.append(i)
        # print(indices_in)

        for index in indices_in:
            new_text = "("
            variable = elements[index-1]
            data = elements[index+1]
            data = data.replace("[","").replace("]","")
            data = data.split(",")
            for d in data:
                new_text = new_text + variable + "==" + d
                if d != data[len(data)-1]:
                    new_text += "|"
                else:
                    new_text += ")"
            elements[index] = ""
            elements[index + 1] = ""
            elements[index-1] = new_text
        result = "\n".join(elements)

        result = result.replace("\n","")
        result = result.replace(" ","")
        condition_as_string = result.replace("\\","")
        # print(result)

        bit_operators_and_or_not = ["&","|","!"]
        awk_operators_and_or_not = ["&&","||","!"]
        operators = [">","<",">=","<=","==","!=","~"]
        names = self.__names_current__()
        names = self.values(clear = False)
        names = np.array(names.replace("\n","").split(self.delimiter))
        for i in range(len(names)):
            condition_as_string = condition_as_string.replace(names[i],"$" + str(i+1))

        for i in range(len(bit_operators_and_or_not)):
            condition_as_string = condition_as_string.replace(awk_operators_and_or_not[i],bit_operators_and_or_not[i])

        for i in range(len(bit_operators_and_or_not)):
            condition_as_string = condition_as_string.replace(bit_operators_and_or_not[i],awk_operators_and_or_not[i])

        command = """awk '
        BEGIN {
            FS = ","
            column = column+1
        }
        {
            if (NR == 1){
                print $0
            }else{
                if (""" + condition_as_string + """){
                    print $0
                }else{

                }

            }
        }
        END {}
        ' """
        awk_command = Awk_command()
        awk_command.command = command
        awk_command.priority = 1
        awk_command.type = "selection"
        self.commands.append(awk_command)
        __ddf__ = deepcopy(self)
        __ddf__.__settle_commands__()
        self.clear_commands()
        return __ddf__

    def modify_column(self,equation):

        equation = equation.replace(" in ["," _in_ [")

        operators = [">=","<=",">","<","==","=","!=","~"," ","&&","\|\|","&","\|","!","(",")"]
        text = "echo \"" + equation + "\" | "
        for operator in operators:
            text = text + "awk 'BEGIN{FS = \"" + operator + "\"}{print($1);for (i=2;i<=NF;i++){if (FS!=\" \"){print (FS)};print($i)}}' | "

        command = text
        command = command + """awk '
        {if ($0 ~ /^[0-9]*[.][0-9]*$/)
            {
                if ($0 ~ /^[.][0-9]*$/){
                    print("0"  $0 "")
                }else{
                    printf($0)
                    print("")
                }
            }else{print($0)}}
        '"""
        # print(command)
        result = os.popen(command).read()
        result = result.replace("\n\n","\n")
        result = result.replace("\n\n","\n")
        result = result.replace("\n\n","\n")
        result = result.replace("\n\n","\n")
        result = result.replace("\n\n","\n")

        elements = result.split("\n")
        # print(result)
        indices_in = []
        for i in range(len(elements)):
            if elements[i] == "_in_":
                indices_in.append(i)
        # print(indices_in)

        for index in indices_in:
            new_text = "("
            variable = elements[index-1]
            data = elements[index+1]
            data = data.replace("[","").replace("]","")
            data = data.split(",")
            for d in data:
                new_text = new_text + variable + "==" + d
                if d != data[len(data)-1]:
                    new_text += "|"
                else:
                    new_text += ")"
            elements[index] = ""
            elements[index + 1] = ""
            elements[index-1] = new_text
        result = "\n".join(elements)

        result = result.replace("\n","")
        result = result.replace(" ","")
        equation = result.replace("\\","")
        # print(result)

        bit_operators_and_or_not = ["&","|","!"]
        awk_operators_and_or_not = ["&&","||","!"]
        operators = [">","<",">=","<=","==","!=","~"]
        names = self.__names_current__()
        names = self.values(clear = False)
        names = np.array(names.replace("\n","").split(self.delimiter))
        for i in range(len(names)):
            equation = equation.replace(names[i],"$" + str(i+1) + "")

        for i in range(len(bit_operators_and_or_not)):
            equation = equation.replace(awk_operators_and_or_not[i],bit_operators_and_or_not[i])

        for i in range(len(bit_operators_and_or_not)):
            equation = equation.replace(bit_operators_and_or_not[i],awk_operators_and_or_not[i])
        equation = equation.split("=")
        column_to_modify = equation[0].strip()
        equation = equation[1].strip()
        command = """awk '
        BEGIN {
            FS = \"""" + self.delimiter + """\"
            RS = "record_delimiter"
            RS_new = "record_delimiter_transform"
        }
        {
            if (NR == 1){
                print $0
            }else{
                for (i = 1;i<=NF;i++){
                    if (i == """ +  column_to_modify.replace("$","") + """){
                        if (i < NF){
                            printf("%s""" + self.delimiter + """\",""" + equation + """)
                        }else{
                            printf("%s",""" + equation + """)
                        }

                    }else{
                        if (i < NF){
                            printf("%s""" + self.delimiter + """\",$i)
                        }else{
                            printf("%s",$i)
                        }
                    }
                }
                printf("%s" RS_new,"")

            }
        }
        END {}
        ' """
        awk_command = Awk_command()
        awk_command.command = command
        awk_command.priority = 1
        awk_command.type = "selection"
        self.commands.append(awk_command)
        __ddf__ = deepcopy(self)
        __ddf__.__settle_commands__()
        self.clear_commands()
        return __ddf__

    def to_csv(self,path_output):
        command = "xargs -I {} echo {}>" + path_output
        awk_command = Awk_command()
        awk_command.command = command
        awk_command.priority = 999999999999
        awk_command.type = "to_csv"
        awk_command.persistance_in_time = "instance"
        self.commands.append(awk_command)
        self.values()
        self.path = path_output
        self.clear_all_commands()
