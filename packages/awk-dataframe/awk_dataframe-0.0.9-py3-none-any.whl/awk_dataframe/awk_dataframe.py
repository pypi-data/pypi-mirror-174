import subprocess
import numpy as np
import pandas as pd
from copy import deepcopy
import time
import sys
import os
import numpy_dataframe as npd
import random
import string

def note(text,print_ = False):
    if print_:
        print(text)

def debug(text,print_ = True):
    if print_:
        print(text)

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

class Conditional_equation:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self):
        super(Conditional_equation, self).__setattr__('condition', True)
        super(Conditional_equation, self).__setattr__('equation', "")
        super(Conditional_equation, self).__setattr__('__columns__', [])

    def __getattr__(self, name):
        return super(Conditional_equation, self).__getattr__(name)
    def __setattr__(self, name, value):
        if name == "equation":
            equation = value.replace(" in ["," _in_ [")

            operators = [">=","<=",">","<","==","=","!=","~"," ","&&","||","&","|","!","(",")"]
            text = "echo \"" + equation + "\" | "
            for operator in operators:
                text = text + "gawk 'BEGIN{FS = \"" + operator + "\"}{print($1);for (i=2;i<=NF;i++){if (FS!=\" \"){print (FS)};print($i)}}' | "

            command = text
            command = command + """gawk '
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
            names = self.__columns__
            for i in range(len(names)):
                equation = equation.replace(names[i],"$" + str(i+1) + "")

            for i in range(len(bit_operators_and_or_not)):
                equation = equation.replace(awk_operators_and_or_not[i],bit_operators_and_or_not[i])

            for i in range(len(bit_operators_and_or_not)):
                equation = equation.replace(bit_operators_and_or_not[i],awk_operators_and_or_not[i])



            value = equation

        if name == "condition":
            condition = value.replace(" in ["," _in_ [")

            operators = [">=","<=",">","<","==","!=","~"," ","&&","||","&","|","!","(",")"]
            text = "echo \"" + condition + "\" | "
            for operator in operators:
                text = text + "gawk 'BEGIN{FS = \"" + operator + "\"}{print($1);for (i=2;i<=NF;i++){if (FS!=\" \"){print (FS)};print($i)}}' | "

            command = text
            command = command + """gawk '
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
    #         print(command)
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
            condition = result.replace("\\","")
            # print(result)

            bit_operators_and_or_not = ["&","|","!"]
            awk_operators_and_or_not = ["&&","||","!"]
            operators = [">","<",">=","<=","==","!=","~"]
            names = self.__columns__
            for i in range(len(names)):
                condition = condition.replace(names[i],"$" + str(i+1))

            for i in range(len(bit_operators_and_or_not)):
                condition = condition.replace(awk_operators_and_or_not[i],bit_operators_and_or_not[i])

            for i in range(len(bit_operators_and_or_not)):
                condition = condition.replace(bit_operators_and_or_not[i],awk_operators_and_or_not[i])
            value = condition

        super(Conditional_equation, self).__setattr__(name, value)


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
        super(Awk_command, self).__setattr__('output_header', -1)
        super(Awk_command, self).__setattr__('has_header', -1)
        super(Awk_command, self).__setattr__('nrow_selected', 0)
        super(Awk_command, self).__setattr__('ncol_selected', 0)
        super(Awk_command, self).__setattr__('nrow_before', 0)
        super(Awk_command, self).__setattr__('ncol_before', 0)
        super(Awk_command, self).__setattr__('path_temp_file', "")


    def __getattr__(self, name):
        return super(Awk_command, self).__getattr__(name)
    def __setattr__(self, name, value):
        super(Awk_command, self).__setattr__(name, value)


    def __copy__(self):
        cls = self.__class__
        com = cls.__new__(cls)
        com.__dict__.update(self.__dict__)
        self.has_been_copied = True
        com.has_been_copied = True
        return com

    def __deepcopy__(self,memo):
        cls = self.__class__
        com = cls.__new__(cls)
        memo[id(self)] = com
        for k, v in self.__dict__.items():
            setattr(com, k, deepcopy(v, memo))

        # com = Awk_command()
        # com.command = self.command
        # com.priority = self.priority
        # com.type = self.type
        # com.persistance_in_time = self.persistance_in_time
        # com.persistance_after_execution = self.persistance_after_execution
        # com.id = self.id
        # com.output_header = self.output_header
        # com.has_header = self.has_header
        # com.nrow_selected = self.nrow_selected
        # com.ncol_selected = self.ncol_selected
        # com.nrow_before = self.nrow_before
        # com.ncol_before = self.ncol_before
        return com

class DataFrame:
    # __names_attributes__ = ["__path__","__has_header__","__commands__","__delimiter__","__id__","__ncol__","__nrow__","__ncol_original__","__nrow_original__","__columns__","__selected_columns__","__nrow_modified_to_unknown_value__"]
    def __repr__(self):
        text = self.__head_current__().execute()
        if self.__nrow__ > 10:
            text = text + "..."
        return text
    def __str__(self):
        text = self.__head_current__().execute()
        if self.__nrow__ > 10:
            text = text + "..."
        return text
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self):
        super(DataFrame, self).__setattr__('__path__', "")
        super(DataFrame, self).__setattr__('__has_header__',True)
        super(DataFrame, self).__setattr__('__commands__', [])
        super(DataFrame, self).__setattr__('__num_copies_commands__', {})
        super(DataFrame, self).__setattr__('__delimiter__', ",")
        super(DataFrame, self).__setattr__('__id__', get_random_string(20))
        super(DataFrame, self).__setattr__('__ncol__', 0)
        super(DataFrame, self).__setattr__('__nrow__', 0)
        super(DataFrame, self).__setattr__('__ncol_original__', 0)
        super(DataFrame, self).__setattr__('__nrow_original__', 0)
        super(DataFrame, self).__setattr__('__columns__', [])
        super(DataFrame, self).__setattr__('__selected_columns__', [])
        super(DataFrame, self).__setattr__('__nrow_modified_to_unknown_value__', True)
        super(DataFrame, self).__setattr__('__string_delimiter__', "\"")


    # def __copy__(self):
    #     cls = self.__class__
    #     result = cls.__new__(cls)
    #     result.__dict__.update(self.__dict__)
    #     return result
    #     # print(type(self))
    #     # print(super(DataFrame, self))
    #     # __ddf_new__ = DataFrame()
    #     # for name in DataFrame.__names_attributes__:
    #     #     # super(DataFrame, __ddf_new__).__setattr__(name,super(DataFrame, self).__getattr__(name))
    #     #     __ddf_new__.__setattr__(name,self.__getattr__(name))
    #     # __ddf_new__.commands = []
    #     # # __ddf_new__.__ncol__ = __ddf_new__.__ncol_original__
    #     # # __ddf_new__.__nrow__ = __ddf_new__.__ncol_original__
    #     # for command in self.__commands__:
    #     #     com = command.___copy__()
    #     #     __ddf_new__.commands.append(com)
    #     # return __ddf_new__

    def __del__(self):
        for command in self.__commands__:
            self.__num_copies_commands__[command.id] -= 1
        self.__clear_all_commands__()



    def __deepcopy_internal__(self,memo):
        # cls = self.__class__
        # result = cls.__new__(cls)
        # memo[id(self)] = result
        # for k, v in self.__dict__.items():
        #     setattr(result, k, deepcopy(v, memo))


    #

        __ddf_new__ = DataFrame()
        # __names_attributes__ = ['__path__',"__has_header__","__commands__","__delimiter__","__id__","__ncol__","__nrow__","__ncol_original__","__nrow_original__","__columns__","__selected_columns__","__nrow_modified_to_unknown_value__"]
        # for name in __names_attributes__:
        #     print(name)
        #     # super(DataFrame, __ddf_new__).__setattr__(name,super(DataFrame, self).__getattr__(name))
        #     # __ddf_new__.__setattr__(name,self.__getattr__(name))
        #     __ddf_new__.name = DataFrame.__getattr__(self,name)
        __ddf_new__.__path__ = self.__path__
        __ddf_new__.__has_header__ = self.__has_header__
        __ddf_new__.__num_copies_commands__ = self.__num_copies_commands__
        __ddf_new__.__delimiter__ = self.__delimiter__
        # __ddf_new__.__id__ = self.__id__
        __ddf_new__.__ncol__ = self.__ncol__
        __ddf_new__.__nrow__ = self.__nrow__
        __ddf_new__.__ncol_original__ = self.__ncol_original__
        __ddf_new__.__nrow_original__ = self.__nrow_original__
        __ddf_new__.__columns__ = self.__columns__
        __ddf_new__.__selected_columns__ = self.__selected_columns__
        __ddf_new__.__nrow_modified_to_unknown_value__ = self.__nrow_modified_to_unknown_value__
        # __ddf_new__.__commands__ = []
        # __ddf_new__.__ncol__ = __ddf_new__.__ncol_original__
        # __ddf_new__.__nrow__ = __ddf_new__.__ncol_original__
        for command in self.__commands__:
            # com = command.___copy__()
            com = deepcopy(command)
            if command.id not in __ddf_new__.__num_copies_commands__.keys():
                __ddf_new__.__num_copies_commands__[command.id] = 0
            __ddf_new__.__num_copies_commands__[command.id] += 1
            __ddf_new__.__commands__.append(com)
        return __ddf_new__

    def __getattr__(self, name):
        # print(name)
        # print(DataFrame.__names_attributes__)
        # if name in DataFrame.__names_attributes__:
        try:
            return super(DataFrame, self).__getattr__(name)
        except:
        # else:
            note("TODO: make another global variable that keeps tracks of current names and use it here and in other column selection options to warn")
            if name in self.__columns__:
                __ddf__ = self.get_cols([name])
                # t = __ddf__.to_npd()
                return __ddf__
            else:
                raise Exception("Column not found")

    def __setattr__(self, name, value):
        # if name != "__names_attributes__":
        # if name in DataFrame.__names_attributes__:
        try:
            super(DataFrame, self).__setattr__(name, value)
        except:
            note("First needs to implement set_rows(rows,Xs)")
        # else:
        #     names = self.names()
        #     if name in names:
        #         print("not yet")


#         if type(value) == list:
#             value = np.array(value)
#         self.d[name] = value
#         super(DataFrame, self).__setattr__('ncol', self.__ncol__ + 1)
#         if self.__nrow__ == 0:
#             super(DataFrame, self).__setattr__('nrow', len(value))
    def __getitem__(self,args):
        note(type(args))
        note("TODO: make another global variable that keeps tracks of current names and use it here and in other column selection options to warn")
        if type(args) == tuple:
            rows,cols=args
            if type(rows) == int:
                rows = [rows]
            if type(cols) == int:
                cols = [cols]

            return self.get_rows(rows).get_cols(cols)
        else:
            cols = args
            if type(cols) == int:
                cols = [cols]
            return self.get_cols(cols)
    #     print("not yet")
#         if type(args) == tuple:

#             if len(key) == 1:
#                 if type(key) == list:
#                     t_ = DataFrame()
#                     for k in key:
#                         DataFrame.__setattr__(t_,k,self.d[k][rows])
#                     return t_
#                 else:
#                     __ddf__ = self.__deepcopy_internal__({})
# __ddf__.__settle_commands__()
# self.__clear_commands__()
# return __ddf__.d[key][rows]
#             else:
#                 t_ = DataFrame()
#                 for k in key:
#                     DataFrame.__setattr__(t_,k,self.d[k][rows])
#                 return t_
#         else:
#             key = args
#             if type(key) == str:
#                 __ddf__ = self.__deepcopy_internal__({})
# __ddf__.__settle_commands__()
# self.__clear_commands__()
# return __ddf__.d[key]
#             else:
#                 if len(key) == 1:
#                     if type(key) == list:
#                         t_ = DataFrame()
#                         for k in key:
#                             DataFrame.__setattr__(t_,k,self.d[k])
#                         return t_
#                     else:
#                         __ddf__ = self.__deepcopy_internal__({})
# __ddf__.__settle_commands__()
# self.__clear_commands__()
# return __ddf__.d[key]
#                 else:
#                     t_ = DataFrame()
#                     for k in key:
#                         DataFrame.__setattr__(t_,k,self.d[k])
#                     return t_

    # def __setitem__(self,key,values):
    #     print("not yet")
#         DataFrame.__setattr__(self,key,values)

    def read_csv(self,path,delimiter = ",",has_header = True,names_columns = [],string_delimiter = "\""):
        if os.path.exists(path):
            if string_delimiter == '"':
                string_delimiter = "\""
            self.__string_delimiter__ = string_delimiter
            self.__path__ = path
            self.__delimiter__ = delimiter
            self.__has_header__ = has_header
            if names_columns != []:
                self.__columns__ = names_columns
            else:
                self.names()
            self.shape()
        else:
            raise Exception("File name does not exists")

    def shape(self):
        if self.__ncol_original__ == 0 and self.__nrow_original__ == 0:
            command = "wc -l " + self.__path__
            result = os.popen(command).read()
            values = result.replace("\n","").strip().split(" ")[0]
            nrow = int(values)
            if self.__has_header__:
                nrow -= 1

            command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' 'BEGIN{}{if (NR>1){exit}}END{print NF}' " + self.__path__
#             print(command)
            result = os.popen(command).read()
            values = result.replace("\n","").strip()
            ncol = int(values)
            values = np.array([nrow,ncol]).astype(int)
            self.__ncol__ = values[1]
            self.__nrow__ = values[0]
            self.__ncol_original__ = ncol
            self.__nrow_original__ = nrow
            return values
        else:
            if self.__nrow_modified_to_unknown_value__:
                shape = self.__shape_current__().execute()
                values = shape.replace("\n","").strip().split(",")
                values = np.array(values).astype(int)
#                 self.__nrow_modified_to_unknown_value__ = False
                self.__ncol__ = values[1]
                self.__nrow__ = values[0]
                self.__ncol_original__ = self.__ncol__
                self.__nrow_original__ = self.__nrow__
                return values
            else:
                return [nrow,ncol]


    def __shape_current__(self,has_header = True):
        command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' -v has_header=has_header_variable " + """'
        BEGIN {

            number_rows = 0
        }
        {
            if (NR == 1){
                if (has_header){
                }else{
                    number_rows+=1
                }

            }else{
                number_rows+=1

            }
        }
        END {
            printf("%s""" + self.__delimiter__ + """",number_rows)
            print(NF)
        }
        ' """

        awk_command = Awk_command()
        awk_command.command = command
        awk_command.priority = 9999999999
        awk_command.type = "shape"
        awk_command.persistance_in_time = "instance"
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1
        return self



    def names(self):
        if len(self.__columns__) == 0:
            if self.__has_header__:
                input = self.__path__
                command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' " + """'
            BEGIN {

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
                self.__columns__ = np.array(result.replace("\n","").split(self.__delimiter__))
                return self.__columns__
            else:
                return []
        else:
            return self.__columns__

#     def __names_current__(self):
#         command = "awk " + """'
#     BEGIN {
#         FS = \"""" + self.__delimiter__ + """\"
#     }
#     {
#         if (NR == 1){
#             print
#             exit
#         }
#     }
#     END {}
#     ' """
#         awk_command = Awk_command()
#         awk_command.command = command
#         awk_command.priority = 9999999999
#         awk_command.type = "names"
#         awk_command.persistance_in_time = "instance"
#         self.__commands__.append(awk_command)
#         return self

    def __to_np_arrays__(self,has_header = True):
        shape = self.shape()
        columns = np.empty(shape[1],list)
        lines = self.values(clear = False)
        lines = lines.split("\n")
        str_types = self.get_types().execute()
        types = []
        types_text = str_types.split(",")
        for type_t  in types_text:
            types.append(eval(type_t))
        line_counter = 0
        names = self.__columns__
        for line in lines:
            if line != "":
                command = "echo '" +line.replace("\n","") + "' | gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' 'BEGIN{}{for (i=1;i<=NF;i++){print($i)}}END{}' "
                result = os.popen(command).read()
                elements = result.split("\n")
                elements = elements[0:len(elements)-1]
                if line_counter == 0:
                        if has_header:
                            names = elements
                        else:
                            for i in range(len(elements)):
                                if len(elements[i]) > 0:
                                    if (elements[i][0] == "\"" and elements[i][len(elements[i])-1] == "\""):
                                        elements[i] = elements[i][1:len(elements[i])-1]
                                try:
                                    columns[i].append(elements[i])
                                except:

                                    columns[i] = [elements[i]]

                else:
                    for i in range(len(elements)):
                        if len(elements[i]) > 0:
                            if (elements[i][0] == "\"" and elements[i][len(elements[i])-1] == "\""):
                                elements[i] = elements[i][1:len(elements[i])-1]
                        try:
                            columns[i].append(elements[i])
                        except:
                            columns[i] = [elements[i]]

                line_counter += 1
        return names,columns,types

    def to_npd(self):
#         names,columns,types = self.__to_np_arrays__()
# #         print(names)
# #         print(columns)
# #         print(types)
#         t = npd.DataFrame()
#         for i in range(len(names)):
#             try:
#                 t[names[i]] = np.array(columns[i]).astype(types[i])
#             except:
#                 try:
#                     t[names[i]] = np.array(columns[i]).astype(float)
#                 except:
#                     t[names[i]] = np.array(columns[i]).astype(str)
        t = npd.DataFrame()
        df = self.to_pandas()
        for name in df.columns:
            t[name] = df[name].values

        return t

    def to_pandas(self):
#         names,columns,types = self.__to_np_arrays__()
# #         print(names)
# #         print(columns)
# #         print(types)
#         df = pd.DataFrame()
#         for i in range(len(names)):
#             try:
#                 df[names[i]] = np.array(columns[i]).astype(types[i])
#             except:
#                 try:
#                     df[names[i]] = np.array(columns[i]).astype(float)
#                 except:
#                     df[names[i]] = np.array(columns[i]).astype(str)
        if not os.path.exists(os.path.expanduser('~') + "/.tmp/"):
            os.mkdir(os.path.expanduser('~') + "/.tmp/")
        if not os.path.exists(os.path.expanduser('~') + "/.tmp/awk_dataframe/"):
            os.mkdir(os.path.expanduser('~') + "/.tmp/awk_dataframe/")
            print("Creating folder ",os.path.expanduser('~') + "/.tmp/awk_dataframe/")
        path_output = os.path.expanduser('~') + "/.tmp/awk_dataframe/output_" + self.__id__ + ".csv"
        self.to_csv(path_output)
        df = pd.read_csv(path_output)
        os.remove(path_output)
        return df


    def execute(self,clear = True,to_file = False,path_sh = ""):
        keep_file = False
        if path_sh == "":
            path_sh = os.path.expanduser('~') + "/.tmp/awk_dataframe/execution_" + self.__id__ + ".sh"
        else:
            keep_file = True

        if self.__has_header__:
            has_header = 1
        else:
            has_header = 0
        output_header = has_header
        # complete_command = "#!/bin/bash\n"
        complete_command = ""
        record_delimiter = "\\n"
        record_delimiter_transform = "\\n"
        intermediate_record_delimiter = "\\n"
        if len(self.__commands__) == 0:
            self.get_rows(range(self.__nrow_original__),return_other_object=False)
            self.__commands__[0].persistance_in_time = "instance"
            self.__commands__[0].persistance_after_execution = "ephemeral"
        for command in self.__commands__:
            if output_header == 0:
                has_header = 0
            if command.has_header != -1:
                if command.has_header == 0:
                    has_header = 0
            if command.output_header != -1:
                if command.output_header == 0:
                    output_header = 0

            if command == self.__commands__[0]:
                if command != self.__commands__[len(self.__commands__)-1]:
                    record_delimiter_transform = "\\n"
                else:
                    record_delimiter_transform = intermediate_record_delimiter
                if command == self.__commands__[len(self.__commands__)-1]:
                    record_delimiter_transform = "\\n"


                if command.type != "to_csv":
                    complete_command += command.command.replace("has_header_variable",str(has_header)).replace("output_header_variable",str(output_header)).replace("record_delimiter_transform",record_delimiter_transform).replace("record_delimiter",record_delimiter) + self.__path__
                else:
                    complete_command += command.command.replace("has_header_variable",str(has_header)).replace("output_header_variable",str(output_header)).replace("record_delimiter_transform",record_delimiter_transform).replace("record_delimiter",record_delimiter)

                record_delimiter = record_delimiter_transform
            else:
                if command != self.__commands__[len(self.__commands__)-1]:
                    record_delimiter_transform = intermediate_record_delimiter
                else:
                    record_delimiter_transform = "\\n"
                # complete_command = complete_command + " | " + command.command.replace("has_header_variable",str(has_header)).replace("output_header_variable",str(output_header)).replace("record_delimiter_transform",record_delimiter_transform).replace("record_delimiter",record_delimiter)
                complete_command = command.command.replace("has_header_variable",str(has_header)).replace("output_header_variable",str(output_header)).replace("record_delimiter_transform",record_delimiter_transform).replace("record_delimiter",record_delimiter) + " <(" + complete_command + ")"
                record_delimiter = record_delimiter_transform
        # ###################using file
        if to_file:
            if not os.path.exists(os.path.expanduser('~') + "/.tmp/"):
                os.mkdir(os.path.expanduser('~') + "/.tmp/")
            if not os.path.exists(os.path.expanduser('~') + "/.tmp/awk_dataframe/"):
                os.mkdir(os.path.expanduser('~') + "/.tmp/awk_dataframe/")
                print("Creating folder ",os.path.expanduser('~') + "/.tmp/awk_dataframe/")

            f = open(path_sh,'w')
            f.write(complete_command)
            f.close()
            result = os.popen("bash " + path_sh).read()
            if not keep_file:
                os.remove(path_sh)
        else:
            result = subprocess.check_output(complete_command, shell=True, executable='/bin/bash').decode()
        # ################

        new_commands = []
        for command in self.__commands__:
            if command.persistance_in_time == "continuous":
                new_commands.append(command)
        self.__commands__ = new_commands
        if clear:
            self.__clear_commands__()
        return result

    def __get_rows_from_to__(self,min_row,max_row,has_header = True,output_header = True,return_other_object = True):

        awk_command = Awk_command()

        if not self.__nrow_modified_to_unknown_value__:
            if min_row < 0:
                min_row = 0
            if max_row > self.__nrow__:
                max_row = self.__nrow__
            awk_command.nrow_selected = max_row-min_col
            awk_command.nrow_before = self.__nrow__
            awk_command.ncol_before = self.__ncol__
            self.__nrow__ = awk_command.nrow_selected

        if self.__nrow__ > 0:
    #         if type(rows) == list:
    #             rows = np.array(rows)
    #         rows_str = np.array2string(rows,separator="\n")
    #         rows_str = rows_str[1:len(rows_str)-1]
    #         path_rows = os.path.expanduser('~') + "/.tmp/awk_dataframe/rows_" + self.__id__ + ".txt"
    #         command = "echo '" + rows_str + "'>" + path_rows
    #         os.system(command)

            variables = "-v has_header=\"has_header_variable\" -v output_header=\"output_header_variable\" -v min_row=\"" + str(min_row) + "\" -v max_row=\"" + str(max_row) + "\" "
            command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' " + variables + """'
            BEGIN {

                RS = "record_delimiter"
                RS_new = "record_delimiter_transform"



            }
            {
                if (has_header){
                    if (FNR == 1){
                        if (output_header){
                            printf("%s" RS_new,$0)
                        }
                    }else{
                        if (FNR >= min_row + 2 && FNR <= max_row + 2){
                            printf("%s" RS_new,$0)
                        }
                    }

                    if (FNR > max_row + 2){
                        exit
                    }
                }else{
                    if (FNR >= min_row + 1 && FNR <= max_row + 1){
                            printf("%s" RS_new,$0)
                    }

                    if (FNR > max_row + 1){
                        exit
                    }
                }

            }
            END {

            }
            ' """
            awk_command.command = command
            if output_header:
                awk_command.output_header = 1
            else:
                awk_command.output_header = 0
            if has_header:
                awk_command.has_header = 1
            else:
                awk_command.has_header = 0
            awk_command.priority = 1
            awk_command.type = "get_rows_range"
            self.__commands__.append(awk_command)
            id_command = awk_command.id
            if id_command not in self.__num_copies_commands__.keys():
                self.__num_copies_commands__[id_command] = 0
            self.__num_copies_commands__[id_command] += 1
            if return_other_object:
                __ddf__ = self.__deepcopy_internal__({})
                __ddf__.__settle_commands__()
                self.__clear_commands__()
                return __ddf__
        else:
            raise Exception("No rows selected")

    def get_rows(self,rows,has_header = True,output_header = True,return_other_object = True):



        if type(rows) == range:
            return DataFrame.__get_rows_from_to__(self,min(rows),max(rows),has_header = has_header,output_header = output_header,return_other_object = return_other_object)
        else:

            awk_command = Awk_command()
            if type(rows) == list:
                rows = np.array(rows)

            if not self.__nrow_modified_to_unknown_value__:
                rows = rows[np.where(np.isin(rows,np.arange(0,nrow)))[0]]
                awk_command = Awk_command()
                awk_command.nrow_selected = len(rows)
                awk_command.nrow_before = self.__nrow__
                awk_command.ncol_before = self.__ncol__
                self.__nrow__ = awk_command.nrow_selected

            rows_str = np.array2string(rows,separator="\n")
            rows_str = rows_str[1:len(rows_str)-1]
            if not os.path.exists(os.path.expanduser('~') + "/.tmp/"):
                os.mkdir(os.path.expanduser('~') + "/.tmp/")
            if not os.path.exists(os.path.expanduser('~') + "/.tmp/awk_dataframe/"):
                os.mkdir(os.path.expanduser('~') + "/.tmp/awk_dataframe/")
                print("Creating folder ",os.path.expanduser('~') + "/.tmp/awk_dataframe/")
            path_rows = os.path.expanduser('~') + "/.tmp/awk_dataframe/rows_" + self.__id__ + "_" + awk_command.id + ".txt"
            # note("TODO: modify this to save with bash")
            # command = "echo '" + rows_str + "'>" + path_rows
            # os.system(command)

            variables = "-v has_header=\"has_header_variable\" -v output_header=\"output_header_variable\" -v min_row=\"" + str(min(rows)) + "\" -v max_row=\"" + str(max(rows)) + "\" -v length_rows=\"" + str(len(rows)) + "\" "
            command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' " + variables + """'
            BEGIN {

                RS = "record_delimiter"
                RS_new = "record_delimiter_transform"
                # cmd = "cat \"
                #
                # while (cmd | getline) {
                #     if (has_header){
                #         rows["1"] = 1
                #         rows[$0+2] = 1;
                #     }else{
                #         rows[$0+1] = 1;
                #     }
                #
                # }
                #
                # close(cmd)



            }
            {
                if (FNR == NR){
                    if(has_header){
                        rows["1"] = 1
                        rows[$0+2] = 1

                    }else{

                        rows[$0+1] = 1
                    }

                }else{
                    if (has_header){
                        if (rows[FNR] == 1){
                            if (FNR == 1){
                                if (output_header){
                                    printf("%s" RS_new,$0)
                                }
                            }else{
                                printf("%s" RS_new,$0)
                            }
                        }
                        if (FNR > max_row + 2){
                            exit
                        }
                    }else{
                        if (rows[FNR] == 1){

                            printf("%s" RS_new,$0)
                                                }
                        if (FNR > max_row + 1){
                            exit
                        }

                    }
                }

            }
            END {

            }
            ' <(echo '""" + rows_str + """') """
            awk_command.command = command
            awk_command.path_temp_file = path_rows
            if output_header:
                awk_command.output_header = 1
            else:
                awk_command.output_header = 0
            if has_header:
                awk_command.has_header = 1
            else:
                awk_command.has_header = 0
            awk_command.priority = 1
            awk_command.type = "get_rows"
            self.__commands__.append(awk_command)
            id_command = awk_command.id
            if id_command not in self.__num_copies_commands__.keys():
                self.__num_copies_commands__[id_command] = 0
            self.__num_copies_commands__[id_command] += 1
            if return_other_object:
                __ddf__ = self.__deepcopy_internal__({})
                __ddf__.__settle_commands__()
                self.__clear_commands__()
                return __ddf__

    def get_cols(self,cols,has_header = True,output_header = True):
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
        # if not self.__nrow_modified_to_unknown_value__:
        cols = cols[np.where(np.isin(cols,np.arange(0,self.__ncol__)))[0]]
        awk_command = Awk_command()
        awk_command.ncol_selected = len(cols)
        awk_command.nrow_before = self.__nrow__
        awk_command.ncol_before = self.__ncol__
        self.__ncol__ = awk_command.ncol_selected

        cols_str = np.array2string(cols,separator="\n")
        cols_str = cols_str[1:len(cols_str)-1]
        if not os.path.exists(os.path.expanduser('~') + "/.tmp/"):
            os.mkdir(os.path.expanduser('~') + "/.tmp/")
        if not os.path.exists(os.path.expanduser('~') + "/.tmp/awk_dataframe/"):
            os.mkdir(os.path.expanduser('~') + "/.tmp/awk_dataframe/")
            print("Creating folder ",os.path.expanduser('~') + "/.tmp/awk_dataframe/")
        path_cols = os.path.expanduser('~') + "/.tmp/awk_dataframe/cols_" + self.__id__ + "_" + awk_command.id + ".txt"
        # note("TODO: modify this to save with bash")
        # command = "echo '" + cols_str + "' | sort | xargs -I {} echo \"{}\" >" + path_cols
        # os.system(command)

        variables = "-v has_header=\"has_header_variable\" -v output_header=\"output_header_variable\" -v min_col=\"" + str(min(cols)) + "\" -v max_col=\"" + str(max(cols)) + "\" "
        command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' " + variables + """'
        BEGIN {
            RS = "record_delimiter"
            RS_new = "record_delimiter_transform"

        }
        {
            if (FNR==NR){
                cols[$0+1] = 1
            }else{
                if (has_header){
                    if (FNR == 1){
                        if (output_header){
                            for (i=min_col+1;i<max_col+1;i++){
                                if (cols[i] == 1){
                                    printf("%s""" + self.__delimiter__ + """", $i)
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
                                printf("%s""" + self.__delimiter__ + """", $i)
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
                            printf("%s""" + self.__delimiter__ + """", $i)
                        }
                    }
                    if (cols[max_col+1] == 1){
                        printf("%s", $(max_col+1))
                    }
                    printf("%s" RS_new,"")
                }
            }

        }
        END {

        }
        ' <(echo '""" + cols_str + """') """
        awk_command.command = command
        awk_command.path_temp_file = path_cols
        if output_header:
                awk_command.output_header = 1
        else:
            awk_command.output_header = 0
        if has_header:
                awk_command.has_header = 1
        else:
            awk_command.has_header = 0
        awk_command.priority = 2
        awk_command.type = "get_cols"
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1

        __ddf__ = self.__deepcopy_internal__({})
        __ddf__.__settle_commands__()
        self.__clear_commands__()
        return __ddf__

    def __clear_commands__(self):
        new_commands = []
        for command in self.__commands__:
            if command.persistance_after_execution != "ephemeral":
                new_commands.append(command)
            else:
                if command.type == "get_cols":
                    self.__ncol__ = self.__ncol_original__
                if command.type == "get_rows":
                    self.__nrow__ = self.__nrow_original__
                # print("num_copies ",command.num_copies)
                if command.type == "get_cols" and self.__num_copies_commands__[command.id] <= 0:
                    path_cols = os.path.expanduser('~') + "/.tmp/awk_dataframe/cols_" + self.__id__ + "_" + command.id + ".txt"
                    if os.path.exists(path_cols):
                        # print("restore os.remove")
                        os.remove(path_cols)

                if command.type == "get_rows" and self.__num_copies_commands__[command.id] <= 0:
                    path_rows = os.path.expanduser('~') + "/.tmp/awk_dataframe/rows_" + self.__id__ + "_" + command.id + ".txt"
                    if os.path.exists(path_rows):
                        # print("restore os.remove")
                        os.remove(path_rows)

                self.__num_copies_commands__[command.id] -= 1



        self.__commands__ = new_commands

    def __clear_all_commands__(self):
        for command in self.__commands__:
            if command.type == "get_cols":
                self.__ncol__ = self.__ncol_original__
            if command.type == "get_rows":
                self.__nrow__ = self.__nrow_original__
            # print("num_copies b ",command.num_copies)
            if command.type == "get_cols" and self.__num_copies_commands__[command.id] <= 0:
                path_cols = os.path.expanduser('~') + "/.tmp/awk_dataframe/cols_" + self.__id__ + "_" + command.id + ".txt"
                if os.path.exists(path_cols):
                    # print("restore os.remove")
                    os.remove(path_cols)

            if command.type == "get_rows" and self.__num_copies_commands__[command.id] <= 0:
                path_rows = os.path.expanduser('~') + "/.tmp/awk_dataframe/rows_" + self.__id__ + "_" + command.id + ".txt"
                if os.path.exists(path_rows):
                    # print("restore os.remove")
                    os.remove(path_rows)

            self.__num_copies_commands__[command.id] -= 1

        self.__commands__ = []

    def __settle_commands__(self):
        for command in self.__commands__:
            command.persistance_after_execution = "permanent"

    def get_types(self,n = 1000):
        note("TODO: missing checking for header")
        awk_command = Awk_command()
        command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' " + """'
        BEGIN {

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
                    if ($i == ""){
                        types[$i] = "str"
                    }else{
                        if ($i ~ /^[0-9]+$/ && types[$i] == "int"){
                            types[$i] = "int"
                        }else{
                            if (($i ~ /^[0-9]*[.][0-9]+$/ || $i=="Nan" || $i=="nan" || $i=="NaN" || $i=="NAN") && (types[$i] == "int" || types[$i] == "float")){
                                types[$i] = "float"
                            }else{
                                types[$i] = "str"
                            }
                        }
                    }
                }
                if (NR > """ + str(n) + """){
                    exit
                }

            }
        }
        END {
            for (i=1;i<NF;i++){
                printf("%s""" + self.__delimiter__ + """",types[$i])
            }
            printf("%s",types[$NF])
            print("")
        }
        ' """

        awk_command.command = command
        awk_command.priority = 9999999999
        awk_command.type = "get_cols"
        awk_command.persistance_in_time = "instance"
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1
        __ddf__ = self.__deepcopy_internal__({})
        __ddf__.__settle_commands__()
        self.__clear_commands__()
        return __ddf__

    def head(self,n=10):
        awk_command = Awk_command()
        command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' " + """'
        BEGIN {

        }
        {
            if (NR < """ + str(n+2) + """){
                print
            }else{
                exit
            }
        }
        END {}
        ' """ + self.__path__


#         awk_command.command = command
#         awk_command.priority = 9999999999
#         awk_command.type = "get_cols"
#         awk_command.persistance_in_time = "instance"
#         self.__commands__.append(awk_command)
#         __ddf__ = self.__deepcopy_internal__({})
# __ddf__.__settle_commands__()
#     self.__clear_commands__()
# return __ddf__
        result = os.popen(command).read()
        return result

    def __head_current__(self,n=10):
        awk_command = Awk_command()
        command = "gawk -v FPAT='([^" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + ")' " + """'
        BEGIN {

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
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1
        return self

    def select(self,condition,has_header = True,output_header = True):
        if type(condition) == str:
            conditional_equation = Conditional_equation()
            conditional_equation.__columns__ = self.__columns__
            conditional_equation.condition = condition
        else:
            conditional_equation = Conditional_equation()
            conditional_equation.__columns__ = self.__columns__
            conditional_equation.equation = equation.equation
            conditional_equation.condition = equation.condition

        self.__nrow_modified_to_unknown_value__ = True


#         print(condition)
        command = """gawk -v FPAT='([^""" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + """)' '
        BEGIN {

            column = column+1
        }
        {
            if (NR == 1){
                print $0
            }else{
                if (""" + conditional_equation.condition + """){
                    print $0
                }else{

                }

            }
        }
        END {}
        ' """

#         print(command)
        awk_command = Awk_command()
        awk_command.command = command
        awk_command.priority = 1
        awk_command.type = "selection"
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1
        __ddf__ = self.__deepcopy_internal__({})
        __ddf__.__settle_commands__()
        self.__clear_commands__()
        return __ddf__

    def modify(self,equation):
        if type(equation) == str:
            note("TODO: allow to use | to determine condition and ; to separate equations")
            conditional_equation = Conditional_equation()
            conditional_equation.__columns__ = self.__columns__
            conditional_equation.equation = equation
        elif type(equation) == Conditional_equation:
            conditional_equation = Conditional_equation()
            conditional_equation.__columns__ = self.__columns__
            conditional_equation.equation = equation.equation
            conditional_equation.condition = equation.condition

        note("TODO: insert in awk statement the possible condition")
        equation = conditional_equation.equation.split("=")
        column_to_modify = equation[0].strip()
        equation = equation[1].strip()
        command = """gawk -v FPAT='([^""" + self.__delimiter__ + "]*)|(" + self.__string_delimiter__ + "[^" + self.__string_delimiter__ + "]+" + self.__string_delimiter__ + """)' '
        BEGIN {

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
                            printf("%s""" + self.__delimiter__ + """\",""" + equation + """)
                        }else{
                            printf("%s",""" + equation + """)
                        }

                    }else{
                        if (i < NF){
                            printf("%s""" + self.__delimiter__ + """\",$i)
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
        self.__commands__.append(awk_command)
        id_command = awk_command.id
        if id_command not in self.__num_copies_commands__.keys():
            self.__num_copies_commands__[id_command] = 0
        self.__num_copies_commands__[id_command] += 1
        __ddf__ = self.__deepcopy_internal__({})
        __ddf__.__settle_commands__()
        self.__clear_commands__()
        return __ddf__

    def to_csv(self,path_output,append=False,__clear_all_commands__ = False,set_as_new_path = False,remove_escape_quotes=False,remove_all_quotes = False):
        if not append:
            if len(self.__commands__) == 0:
                self.get_rows(range(self.__nrow_original__),return_other_object=False)
                self.__commands__[0].persistance_in_time = "instance"
                self.__commands__[0].persistance_after_execution = "ephemeral"
            if remove_escape_quotes:
                command = "gawk '{gsub(/^\"|\",|,\"|\"$/,\"\");print $0 >\"" + path_output + "\"}' "
            elif remove_all_quotes:
                command = "gawk '{gsub(/\"/,\"\");print $0 >\"" + path_output + "\"}' "
            else:
                command = "gawk '{print $0 >\"" + path_output + "\"}' "
            awk_command = Awk_command()
            awk_command.command = command
            awk_command.priority = 999999999999
            awk_command.type = "to_csv"
            awk_command.persistance_in_time = "instance"
            self.__commands__.append(awk_command)
            id_command = awk_command.id
            if id_command not in self.__num_copies_commands__.keys():
                self.__num_copies_commands__[id_command] = 0
            self.__num_copies_commands__[id_command] += 1
            self.execute()

            if set_as_new_path:
                self.__path__ = path_output
            if __clear_all_commands__:
                self.__clear_all_commands__()
        else:
            if remove_escape_quotes:
                command = "gawk '{gsub(/^\"|\",|,\"|\"$/,\"\");print $0 >>\"" + path_output + "\"}' "
            elif remove_all_quotes:
                command = "gawk '{gsub(/\"/,\"\");print $0 >>\"" + path_output + "\"}' "
            else:
                command = "gawk '{print $0 >>\"" + path_output + "\"}' "
            awk_command = Awk_command()
            awk_command.command = command
            awk_command.priority = 999999999999
            awk_command.type = "to_csv"
            awk_command.persistance_in_time = "instance"
            self.__commands__.append(awk_command)
            id_command = awk_command.id
            if id_command not in self.__num_copies_commands__.keys():
                self.__num_copies_commands__[id_command] = 0
            self.__num_copies_commands__[id_command] += 1
            self.execute()
            if set_as_new_path:
                self.__path__ = path_output
            if __clear_all_commands__:
                self.__clear_all_commands__()
