# -*- coding: utf-8 -*-

need_events = ['tour', 'kids', 'theater', 'show', 'party', 'exhibition',
               'concert', 'education', 'romance', 'permanent-exhibitions',
               'circus', 'comedy-club', 'stand-up', 'yoga', 'fashion', 'holiday',
               'evening', 'games', 'festival', 'quest', 'night', 'sport', 'photo',
               'fair', 'cinema']


# tour -> excursions

# замена русских названий

def prepare_categories(main_array, categories_array_eng, categories_array_rus):
    # по дням
    for index, i in enumerate(main_array):
        # по категориям в день
        for index1, j in enumerate(i):
            # по событиям в категории

            for index2, k in enumerate(j):
                if (k['categoriesrus'] == u"Детские"):
                    main_array[index][index1][index2]['categoriesrus'] = u"Детские мероприятия"

                if (k['categoriesrus'] == u"Comedy club / Камеди клаб"):
                    main_array[index][index1][index2]['categoriesrus'] = u"Камеди клаб"

                if (k['categoriesrus'] == u"Stand up shows"):
                    main_array[index][index1][index2]['categoriesrus'] = u"Stand Up Шоу"

                if (k['categoriesrus'] == u"Театр"):
                    main_array[index][index1][index2]['categoriesrus'] = u"Театры"

                if (k['categories'] == u"tour"):
                    main_array[index][index1][index2]['categories'] = u"excursions"

    try:
        categories_array_eng[categories_array_eng.index(u"tour")] = u"excursions"
    except:
        None

    try:
        categories_array_rus[categories_array_rus.index(u"Театр")] = u"Театры"
    except:
        None

    try:
        categories_array_rus[categories_array_rus.index(u"Stand up shows")] = u"Stand Up Шоу"
    except:
        None

    try:
        categories_array_rus[categories_array_rus.index(u"Детские")] = u"Детские мероприятия"
    except:
        None

    try:
        categories_array_rus[categories_array_rus.index(u"Comedy club / Камеди клаб")] = u"Камеди клаб"
    except:
        None

    for i in xrange(len(categories_array_eng)):
        categories_array_eng[i] = categories_array_eng[i].replace("-", "")

    return main_array, categories_array_eng, categories_array_rus
