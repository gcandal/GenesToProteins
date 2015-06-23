//
//  main.c
//  IOPE
//
//  Created by José Pedro Moreira on 22/04/15.
//  Copyright (c) 2015 José Pedro Moreira. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <sqlite3.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#define tablesQuery "SELECT name FROM sqlite_master WHERE type='table';"
#define columnsQuery "PRAGMA table_info(%s);"
#define tablesArraySize 100
#define columnArraySize 100
#define fileNameBuffSize 512
#define selectStringSize 256
#define pathStringSize 512

#define end(x) x[strlen(x)]
#define last(x) x[strlen(x)-1]
#define first(x) x[0]

#define mode_param argv[1]
#define dir_param argv[3]
#define db_param argv[2]

#define csv_mode(x)  x & to_csv
#define prolog_mode(x) x & to_prolog


typedef enum{
    
    
    to_prolog = 1,
    to_csv = 2,
    to_both = 3
    
    
} op_mode;

sqlite3 * dbHandle;
op_mode running_mode;


typedef char * name;
typedef name* table_list;
typedef name* column_list;

table_list tables_getAll();
void list_free(table_list tablesArray);
void list_free(column_list colsArray);
char ** columns_getAll(name tableName);
int suitableDir(const char * dirPath);

void stringByAppendingPathComponent(const char * original,const char * component,char * result);
void csv_write_rows(char * selectString,FILE * f);
void csv_write_column_names(column_list cols,FILE *f);
int setMode(const char * mode);
void prolog_write_rows(name relationName,char * selectString,FILE *f);

int main(int argc, const char * argv[]) {
    
    
    if(argc != 4){        
        printf("Wrong Number of Parameters!\n");
        return -1;        
    }
    
    
    
    int result = sqlite3_open(db_param, &dbHandle);
    printf("%i\n", sqlite3_extended_errcode(dbHandle));
    if (result != SQLITE_OK) {
        printf("Specified File is not a proper db!\n");
        return -2;
    }
    
    
    if (!suitableDir(dir_param)) {
        printf("The specified path is not a directory\n");
        return  -3;
    }
    
    
    if(!setMode(mode_param)){
        
        printf("Invalid mode provided\n");
        return -4;
        
    }
    
    
    
    
    
    
    
    
    
    table_list tables = tables_getAll();//get the tables
    int index = 0;
    name tableName = NULL;
    
    
    while((tableName=tables[index++]) != NULL){
        
        
        char filePath[fileNameBuffSize];   

        
        
        char selectString[selectStringSize];
        
        sprintf(selectString, "SELECT * from %s;",tableName);
        
        
        column_list cols = columns_getAll(tableName);
        
        
        if (csv_mode(running_mode)) {
            
            char fileName [fileNameBuffSize];
            
            sprintf(fileName, "%s.csv",tableName);
            
            stringByAppendingPathComponent(dir_param, fileName, filePath);
            FILE *f_csv = fopen(filePath, "wb");
            csv_write_column_names(cols,f_csv);
            csv_write_rows(selectString,f_csv);
            fclose(f_csv);
        }
        
        if (prolog_mode(running_mode)){
            
            
            char fileName [fileNameBuffSize];
            
            sprintf(fileName, "%s.prolog",tableName);
            
            stringByAppendingPathComponent(dir_param, fileName, filePath);
            FILE *f_prolog = fopen(filePath, "wb");
            prolog_write_rows(tableName, selectString, f_prolog);
            
            
        }
        
        
        
        
        
        
        list_free(cols);
        
    }
    
    list_free(tables);

    

    return 0;
}


#pragma mark - Tables and Columns Operations

table_list tables_getAll(){
    
    
    sqlite3_stmt *statement;
    
    char ** tableNames = malloc(tablesArraySize*sizeof(char *));//safe to assume no more than 100 tables
    
    int pos = 0;
    
    // prepare our query
    sqlite3_prepare_v2(dbHandle, tablesQuery, -1, &statement, 0);
    
    
    while (sqlite3_step(statement) == SQLITE_ROW && pos + 1 < tablesArraySize)//dont overflow the array!
    {
        // retrieve the value of the first column (0-based)
        const unsigned char * tableName = sqlite3_column_text(statement, 0);
        
        char * occurrence = strstr((const char *)tableName, "sqlite_");
        
        if((const unsigned char *)occurrence == tableName)continue; // if the table name starts with sqlite_ then dont include it (internal sqlite table)
        
        char * tableNameCopy = malloc(strlen((char *)tableName)*sizeof(char));//alloc array

        
        strcpy(tableNameCopy,(char *)tableName);

        tableNames[pos++] = tableNameCopy;
    }
    
    
    tableNames[pos] = NULL;
    // free our statement
    sqlite3_finalize(statement);
    
    
    return tableNames;

}

column_list columns_getAll(name tableName){
    
    char ** columnNames = malloc(columnArraySize * sizeof(char *));
    
    sqlite3_stmt *statement;

    
    int pos = 0;
    
    
    char* query = malloc((strlen(tableName)+strlen(columnsQuery))*sizeof(char));
    
    sprintf(query, columnsQuery,tableName);
    
    // prepare our query
    sqlite3_prepare_v2(dbHandle, query, -1, &statement, 0);
    
    
    while (sqlite3_step(statement) == SQLITE_ROW && pos + 1 < columnArraySize)//dont overflow the array!
    {
        // retrieve the value of the first column (0-based)
        const unsigned char * colName = sqlite3_column_text(statement, 1);
        
        char * colNameCopy = malloc(256);//alloc array
        
        
        strcpy(colNameCopy,(char *)colName);
        
        columnNames[pos++] = colNameCopy;
    }
    
    
    columnNames[pos] = NULL;
    // free our statement
    sqlite3_finalize(statement);
    
    free(query);
    
    
    return columnNames;
    
    


}

void list_free(table_list tablesArray){


    
    int i = 0;
    
    name occurrence;

    while ((occurrence = tablesArray[i++]) != NULL) {
        free(occurrence);
    }
    
    
    free(tablesArray);
    
    
}


#pragma mark - Parameter stuff

int suitableDir(const char * dirPath){
    struct stat s;
    
    if (stat(dirPath, &s) != -1 && S_ISDIR(s.st_mode)) {
        return 1;
    }
    return 0;
    
    
}

int setMode(const char * mode){
    
    
    int retVal = 1;
    if (strcmp(mode, "-csv") == 0) running_mode = to_csv;
    else if(strcmp(mode, "-prolog")==0)running_mode = to_prolog;
    else if(strcmp(mode, "-both")==0)running_mode = to_both;
    else retVal = 0;
    
    
    return retVal;
 
    
}

#pragma mark - Helper Methods
void stringByAppendingPathComponent(const char * original,const char * component,char * result){
    strcpy(result, original);
    int pos =(int) strlen(result);
    
    if (last(original)!='/' && first(component)!='/') {//no bars
        result[strlen(result)]='/';
        pos++;
    }
    else if (last(original)=='/' && first(component)=='/'){//both have bars
        
        last(result)='\0';//remove last bar
        pos--;
        
    }
    
    strcpy(&result[pos], component);
    
    
    
    
}


#pragma mark - Prolog operations

void prolog_write_rows(name relationName,char * selectString,FILE *f){
    
    
    sqlite3_stmt * stmt;
    
    
    sqlite3_prepare(dbHandle, selectString, (int)strlen(selectString), &stmt, 0);
    
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        
        const unsigned char * content = NULL;
        int i = 0;
        
        while (1==1) {
            
            content = sqlite3_column_text(stmt, i++);
            
            if (content == NULL) {
                char  *close_bracket_new_line=").\n";
                fwrite(close_bracket_new_line,sizeof(char) ,strlen(close_bracket_new_line), f);
                break;
            }
            
            char comma = ',';
            if (i==1) {
             
                char bracket = '(';
                fwrite(relationName, strlen(relationName), sizeof(char), f);
                fwrite(&bracket, 1, sizeof(char), f);
            }
            if(i!=1)fwrite(&comma, 1, sizeof(char), f);
            fwrite(content, strlen((const char*)content), sizeof(const unsigned char), f);
            
            
            
        }
        
    }
     sqlite3_finalize(stmt);
    
}


#pragma mark - CSV operations

void csv_write_rows(char * selectString,FILE * f){
    
    sqlite3_stmt * stmt;
    
    
    sqlite3_prepare_v2(dbHandle, selectString, (int)strlen(selectString), &stmt, 0);
    
    
    while ( sqlite3_step(stmt) == SQLITE_ROW){// for all rows
        
    
        
        const unsigned char * content = NULL;
        int i = 0;
        
        while (1==1) {
            
            content = sqlite3_column_text(stmt, i++);
            
            if (content == NULL) {
                char newLine ='\n';
                fwrite(&newLine, 1, sizeof(char), f);
                break;
            }
            
            char comma = ',';
            if(i!=1)fwrite(&comma, 1, sizeof(char), f);
            fwrite(content, strlen((const char*)content), sizeof(const unsigned char), f);

        }

        
        
    }
    
    sqlite3_finalize(stmt);
    
    
}


void csv_write_column_names(column_list cols,FILE *f) {
    int col_index = 0;
    name col_name;
    while ((col_name = cols[col_index++])) {
        
        if(col_index!=1){
            char comma = ',';
            fwrite(&comma, 1, sizeof(char), f);
        }
        fwrite(col_name, strlen(col_name), sizeof(char), f);
        
    }
    char newLine = '\n';
    fwrite(&newLine,1, sizeof(char), f);
}