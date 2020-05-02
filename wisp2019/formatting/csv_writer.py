def write_csv(write_dict_list, file_name, order=None):
    try:

        file = open(file_name, 'wb')
        headers = list()

        # Set up the headers for the columns
        #TODO: use the order param if it is present to order the headers
        if order is not None:
            for header in order:
                headers.append(header)

        for row in write_dict_list:
            for header in row.keys():
                if header not in headers:
                    headers.append(header)

        # Write out headers
        headers_str = ""
        for i in range(len(headers)):
            headers_str += str(headers[i]) + ","
        headers_str = headers_str.rstrip(",")
        headers_str += "\n"
        file.write(headers_str.encode('utf8'))

        for row in write_dict_list:
            row_out_str = ""
            for i in range(len(headers)):
                row_out_str += str(row.get(headers[i], ""))
                row_out_str += ","
            row_out_str = row_out_str.rstrip(",")
            row_out_str += "\n"
            file.write(row_out_str.encode('utf8'))

        file.close()

    except Exception as e:
        raise e
    return None