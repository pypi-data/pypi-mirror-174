from wedeliver_core.helpers.sql import sql


def search_function(table_name, search_list, append_extra=None):
    """
    """
    validation_error = []

    def _find_matched(db_results, key, search_item):
        for db_instance in db_results:
            if db_instance.get(key) == search_item.get("search_value"):
                return db_instance
        return None

    for item_dict in search_list:
        # query = db.session.query(model)

        input_group_search_key = item_dict.get('search_key') or "id"

        input_group = item_dict.get('inputs')
        input_group_list = [obj.get("search_value") for obj in input_group]

        # model_key = model.__dict__.get(input_group_search_key)
        # result_db = query.filter(model_key.in_(input_group_list)).all()
        # result_db_list = [obj.__dict__.get(input_group_search_key) for obj in result_db]

        query = """
                SELECT *
                FROM {table_name}
                WHERE {input_group_search_key} IN ('{input_group_list}')
                """.format(
            input_group_list=', '.join(str(value) for value in input_group_list),
            table_name=table_name,
            input_group_search_key=input_group_search_key
        )
        result_db = sql(query)
        result_db_list = [obj.get(input_group_search_key) for obj in result_db]
        # if len(input_group_list) != len(result_db_list):
        for obj in input_group:
            if obj.get("search_value") not in result_db_list:
                error_obj = dict(
                    indexes=obj.get("indexes")
                )
                error_obj[input_group_search_key] = dict(
                    message="{} '{}' is not exists".format(input_group_search_key, obj.get("search_value"))
                )

                validation_error.append(error_obj)
            elif result_db_list.count(obj.get("search_value")) > 1:
                error_obj = dict(
                    indexes=obj.get("indexes")
                )
                error_obj[input_group_search_key] = dict(
                    message="{} '{}' too many exists, can not determine witch one".format(input_group_search_key,
                                                                                          obj.get("search_value"))
                )

                validation_error.append(error_obj)
            else:
                matched_obj = _find_matched(db_results=result_db, key=input_group_search_key, search_item=obj)
                obj.update(dict(
                    matched_id=matched_obj.get("id")
                ))
                if append_extra and isinstance(append_extra, list):
                    for _append_key in append_extra:
                        obj[_append_key] = matched_obj.get(_append_key)

    return search_list, validation_error
