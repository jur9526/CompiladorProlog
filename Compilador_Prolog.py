import os;
import sys;
tipoPredicado="";
global baseH
baseH = [];#Lista donde se almacenaran los hechos
baseR = [];#Lista donde se almacenaran las reglas
inicio = False; #bandera para imprimir la información del compilador solo una vez

#Menu principal del progra, en este se selcciona el modo a utilizar [definición, consulta]
def menu():
    global inicio;
    if (inicio == False):
        print("Welcome to TEC-Prolog (Multi-threaded, 64 bits, Version 7.1.23)")
        print("Copyright (c) 2014 Tecnológico de Costa Rica,Cartago Costa Rica")
        print("TEC-Prolog comes with ABSOLUTELY NO WARRANTY. This is free software,")
        print("and you are welcome to redistribute it under certain conditions.")
        inicio = True;
    #Variable que almacen la opción ingresada por el usuario
    opcion = input ("Seleccione el modo en el que desea trabajar: ")
    #While que valida que la opción ingresada sea valida [define, consult]
    while (1):
        if ((opcion=="<define>") or (opcion=="<consult>") or (opcion=="Exit")):
            break
        else:
            print ("Modo incorrecto, los modos validos son <define> y <consult>\n")
            opcion = input ("Seleccione el modo en el que desea trabajar: ")
    #Si la opción es define entra el modo de definición de predicados
    if (opcion=="<define>"):
        while(True):    
            opcion1 = input ("Inserte el predicado: ")
            if opcion1 == "</define>":
                break
            else:
                predicado(opcion1,True);
        menu()
    elif(opcion == "Exit"):
        ingresarHechos("Exit");
    #Como se valida que la opción debe ser valida si no entra al modo de definición entra al modo de consulta
    else:
        while(True):
            cons=input ("-? ")#Variable que almacena la consulta
            if (cons==""):
                pass
            elif (cons=="</consult>"):#validación para salir del modo consulta
                break
            else:
                consu=evalua(cons)#Variable que almacena el resultado de la consulta
                if isinstance(consu,list):#En caso de hacer backtracking
                    constante=consu[0]
                    c=0
                    for e in consu[1:]:
                        print (constante,": ",e)
                        if (c<=len(cons)):
                            cons=input()
                            if cons==";":#validación para mostrar otro valor de la consulta
                                c+=1
                            elif cons==".":
                                print ("Yes.")
                                break
                            else:
                                print ("Error")
                                break
                        else:
                            print ("Yes.") #Imprime Yes al final de la consulta
                else:
                    if  isinstance(consu,bool): #Si el valor de consu es un booleano
                        if evalua(cons):
                            print ("Yes.")
                        else:
                            print ("No.")
                    else:
                        print (consu) #Imprime el mensaje de error
        menu()
########################################################################################################################

#Función que determina el tipo de predicado (Hecho o Regla)
def predicado(predicado, flag):
    if predicado[0].islower():
        cont = 2;
        contAux = 0;
        parentesis = 0;
        ##Ciclo que determina si el predicado es un hecho
        for i in range(len(predicado)):
            if (predicado[i]=="("):
                cont = cont-1;
                parentesis = parentesis+1;
                contAux = contAux+1;
            if (predicado[i]==")"):
                cont = cont-1;
                contAux = contAux -1;
                parentesis = parentesis+1;

        if (parentesis == 0):
            print ("Predicado incorrecto.")
            return False;

        if (contAux !=0):
            print ("Parentesis mal empleados. Revisar!")
            return False;
        
        ##Si el "if" se cumple, el predicado es una regla o la sintaxis del hecho es invalida.
        if (cont != 0)or(predicado[len(predicado)-1]!= "."):
            global tipoPredicado;
            aux = predicado.split(")")[1];
            if (aux[0:2] == ":-"):
                tipoPredicado = "regla"
                print ("El predicado es una regla");
                tipoPredicado = "regla" 
                sintaxisRegla(predicado,flag);
            else:
                print("Predicado incorrecto")
                return False;
        else:
            tipoPredicado = "hecho";
            sintaxisHecho(predicado,flag);
            return True
    else:
        print("ERROR")
        return False;

#Realiza el análisis léxico y sintáctico del hecho
def sintaxisHecho(predicado, flag):
    ##Valida la sintaxis del hecho
    if predicado[0].islower():
        contParentesis = 2;
        for parentesis in predicado:
            if ((parentesis == "(") or (parentesis == ")")):
                contParentesis = contParentesis-1;
        if (contParentesis !=0):
            return False;
        temp = [];
        contArgs = 1; #aridad del argumento
        argumento = "";
        functor = (predicado.split("(")[0]);
        argumentoAux = (predicado.split("(")[1]);
        ##print(argumento); 

        for aux in functor:
            if ((aux.isalnum() != True) and (aux != "_")):
                print("Sintaxis del hecho incorrecta")
                return False
        #Validación de argumentos
        
        
        if (argumentoAux[0].isupper() and tipoPredicado == "hecho" and flag):
            print ("Error");
            return False;
        else:
            for aux2 in range(len(argumentoAux)):
                if ((argumentoAux[aux2]) == "," and (argumentoAux[aux2+1]!= " ")):
                    if(argumentoAux[aux2+1].isupper() and tipoPredicado=='hecho' and flag):
                        print ("Error")
                        return False;
                if(argumentoAux[aux2].isalnum()!= True and ((argumentoAux[aux2] != ")") or (argumentoAux[aux2] == "."))):
                    if(argumentoAux[aux2] == " "):
                        if ((argumentoAux[aux2-1].isalnum()== True) and (argumentoAux[aux2+1].isalnum())== True):
                            print("Sintaxis del hecho incorrecta")
                            return False;    
                    if (argumentoAux[aux2].isalnum() != True and (argumentoAux[aux2] != "," and  argumentoAux[aux2] != "." and argumentoAux[aux2]!= "_")):
                        print("El caracter: " + argumentoAux[aux2] +",no es valido.")
                        return False;
        
        for aux in argumentoAux:
            if (aux == ")"):
                break;
            else:
                argumento = argumento+aux;
        #Permite determinar la aridad del argumento
        for aux2 in argumento:
            if (aux2 == ","):
                contArgs = contArgs+1;
            if (aux2 == " "):
                argumento.replace(" ","");

        #Ingresa predicado al txt
        listaArgumentos = [];
        if (tipoPredicado == 'hecho' and flag): 
            ingresarHechos(predicado);
            global baseH;
            agmnto =  "";
            for i in argumento:
                if (i == "," or i ==")"):
                    listaArgumentos.append(agmnto)
                    agmnto = "";
                else:
                    agmnto= agmnto+i;
            listaArgumentos.append(agmnto)
                    
            #Ingresa a la lista
            temp = [functor,contArgs,listaArgumentos];
            baseH.append(temp)
            print("Predicado correcto.")
        else:
            return True;
    else:
        print("ERROR")
        return False;

def existeFunctor(hecho):
##En caso de ser regla verifica que el functor haya sido ingresado
    functor = (hecho.split("(")[0]);
    bandera = False;
    largo = len(baseH)-1;
    cont = 0;
    while (cont <= largo):
        if (baseH[cont][0] == functor):
            bandera = True;
            break;
        else:
            cont = cont+1;
    if (bandera == False):
        print ("El functor " + functor + ",no existe ");
        return False;

#Análisis léxico y sintáctico de la regla
def sintaxisRegla(predicado, flag):
    validar = predicado.split(":-")[0]+".";
    validar2 = predicado.split(":-")[1];
    hecho = "";
    if((sintaxisHecho(validar, flag)==True) and (predicado[len(predicado)-1]==".")):
        for aux in range(len(validar2)):

            if (validar2[0] == "."):
                hecho = hecho+".";
                if(sintaxisHecho(hecho,flag)== True):
                    existeFunctor(hecho);
                    ingresarHechos(predicado);
                    break;
                else:
                    print("predicado incorrecto. Ingrese de nuevo")
                    return False;
                
            if(validar2[0]== ")"):
                if ((validar2[0+1] == ",") or (validar2[0+1]==";")):
                    hecho = (hecho + validar2[0]);
                    hecho = hecho+".";
                    validar2 = validar2[2:]; #Quitar la , o ; que queda 
                    if (sintaxisHecho(hecho, flag)== True):
                        existeFunctor(hecho);
                        hecho = "";
                    else:
                        print("predicado incorrecto. Ingrese de nuevo");
                        return False;
                if (validar2[0+1] == "."):
                    hecho = (hecho + validar2[0]);
                    validar2 = validar2[1:];
            else:
                hecho = (hecho + validar2[0]);
                validar2 = validar2[1:];   
    else:
        print("Error en la escritura de la regla")
        return False;

#Ingresa los hechos a la base de conocimientos.    
def ingresarHechos(predicado):
    if (predicado == "Exit"):
        os.unlink("baseConocimientos.txt");
        SystemExit;
    else:
        outfile = open('baseConocimientos.txt', 'a');
        if (tipoPredicado == 'regla'): 
            listaTemp = [predicado];
            baseR.append(listaTemp);
        outfile.write(predicado + '\n');
        print('>>> Agregado a la base de conocimientos.');
        outfile.close();  

##########################################################################################

#Función que acomoda la lista de reglas para facilitar las consultas
def cambia():
    tempL=[] #Variable temporal para no modificar la lista de reglas
    lista=[]
    #for para pasar la información de baseR a TempL con un split 
    for ele in baseR:
        for r in ele:
            tempL.append(r.split("-"))
    c=0
    tempL1=[] #Lista donde se almacenan
    #while para darle formato a las reglas
    while c<len(tempL):
        temp=tempL[c][0]
        tempL1=cambia_predicado(temp)
        tempL1.append(tempL[c][1])
        tempL[c]=tempL1
        temp=""
        L=[]
        flag=True
        for e in tempL[c][3]:
            if e=="(":
                flag=False
                temp+=e
            if e==")":
                flag=True
                temp+=e
            if ((e=="," or e==";" or e==".") and flag):
                temp+=e
                L.append(temp)
                if (e==";" or e==","):
                    L.append(e)
                temp=""
            else:
                if (e=="(" or e==")"):
                    pass
                else:
                    temp+=e
        tempL[c][3]=L
        L=tempL[c][3]
        c1=0
        while (c1<len(L)): #While para darle formato a los hechos dentro de la regla
            if (L[c1]!=";"):
                L[c1]=cambia_predicado(L[c1])
            c1+=1
        c+=1
    baseR2=tempL
    return baseR2   

#Esta función se encarga de resolver consultas de hechos.
def consultaH(var):
    temp1=var[2]
    flag=False #Bandera para determinar si hay variables en la consulta
    back=[]#Lista donde se almacenan los valores en caso de haber variables
    for e in temp1:  #Se determinan si hay variables dentro de la consulta
                if e[0].isupper():
                    back.append(e)
                    flag=True
                    break
    if flag: #En caso de haber variables
        for i in baseH:
            if (i[:-1]==var[:-1]): #Si el funtor y la arirdad son iguales
                temp2=i[2]
                cont=0
                while (cont<var[1]):
                    #Se verifica si la consulta es verdadera
                    if temp1[cont]==temp2[cont]:
                        cont+=1
                    elif (temp1[cont][0].isupper()):
                        back.append(temp2[cont])
                        cont+=1
                    else:
                        break
        return back #Lista con los valores de la consulta
    else:
        for i in baseH:
            if (i[:-1]==var[:-1]):
                temp2=i[2]
                cont=0
                if (temp1==temp2):
                    return True
                res=True
                while (cont<var[1]):
                    #Se verifica si la consulta es correcta
                    if (temp1[cont]==temp2[cont]):
                        cont+=1
                    else:
                        if (temp1[cont]=='_'):
                            cont+=1
                        else:
                            res=False
                            break
                if (res):
                    return True
        return False

#Esta función se encarga de resolver consultas de reglas.
def consultaR(var):
    tempL=cambia()
    resul=[]#Lista que almacena los resultados de los hechos dentro de la consulta
    temp=[]#variable temporal
    flag=False
    flag2=True
    for i in tempL:
        if (i[:-2]==var[:-1]): #Se revisa la aridad y el funtor
            c=0
            while (c<len(i[2])):
                temp.append([var[2][c],i[2][c]])
                c+=1
            for e in i[3]:
                c=0
                if ((e==",") or (e==";")):
                    resul.append(e)
                else:
                    while (c<len(e[2]) ):
                        for t in temp:
                            if t[1]==e[2][c]:
                                e[2][c]=t[0]
                        c+=1
                    tempR=consultaH(e)
                    resul.append(tempR)
    for r in resul:
        if (r==";"):
            flag2=True
        elif (r==","):
            flag2=False
        else:
            if (r):
                flag=True
            else:
                if (flag2):
                    pass
                else:
                    return False
    return flag

#cambia el formato del predicado para poder realizar las consultas
def cambia_predicado(var):
    predicado=[]
    temp=''
    tempL=var.split('(')
    predicado.append(tempL[0])
    aridad=tempL[1].count(',')
    aridad+=1
    predicado.append(aridad)
    variable=[]
    for e in tempL[1][:-2]:
        if (e==","):
            variable.append(temp) 
            temp=''
        else:
            temp+=e
    variable.append(temp)
    predicado.append(variable)
    return predicado

#Función que evalua que la aridad y el predicado sean iguales para proceder a realizar la consulta
def evalua(var):
    if (var[:5]=="write"):
        return write(var)
    else:
        var1 = predicado(var,False);
        if (var1):
            predi=cambia_predicado(var)
            consult=False
            flag=True
            for i in baseH:
                if (predi[0]==i[0] and predi[1]==predi[1]):
                    consult=consultaH(predi)
                    flag=False
            if flag:
                flag=False
                baseR2=cambia()
                for i in baseR2:
                    if (predi[0]==i[0] and predi[1]==predi[1]):
                        consult=consultaR(predi)
            return consult
        else:
            return "Error"
    
def write(sentencia):
    contador=0
    cont3=0
    for elemento in sentencia[5:]:
        if elemento!=")":
            contador+=1
    contador2=contador
    if sentencia[contador:]=="'),nl.":
        strin=""
        for ele in sentencia[7:contador]:
            if ele=="'":
                strin="pe"
        if strin!="pe":
            return sentencia[7:contador] + "\n"
        else:
            return "error lexico"
    elif sentencia[contador+3:]=="').":
        bandera=[]
        bandera2=True
        contador=0
        string=""
        for elemento in sentencia[7:]:
            if elemento=="'":
                bandera2=False
                contador+=1
                bandera+=elemento
            elif elemento==")" and bandera2==False:
                break
            else:
                bandera+=elemento
        for ele in bandera[:-1]:
            if ele.isalpha() or ele.isnumeric():
                string+=ele
            else:
                print("error lexico")
                break
        return string
    else:
        return "error de sintaxis"

menu()
