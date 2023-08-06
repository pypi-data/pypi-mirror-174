from wedeliver_core.helpers.sql import sql


def search_function(table_name, search_list):
    """
    """
    validation_error = []

    def _find_matched(db_results, key, search_item):
        for db_instance in db_results:
            if db_instance.get(key) == search_item.get("search_value"):
                return db_instance.get("id")
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
                validation_error.append(
                    "{} '{}' is not exists".format(input_group_search_key, obj.get("search_value")))
            elif result_db_list.count(obj.get("search_value")) > 1:
                validation_error.append(
                    "{} '{}' too many exists, can not determine witch one".format(input_group_search_key,
                                                                                  obj.get("search_value")))
            else:
                obj.update(dict(
                    matched_id=_find_matched(db_results=result_db, key=input_group_search_key, search_item=obj)
                ))

    return search_list, validation_error
