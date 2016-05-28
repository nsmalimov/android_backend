# -*- coding: utf-8 -*-

need_places = ['museum', 'park', 'restaurants', 'art-centers', 'culture',
               'library', 'books', 'attract', 'gallery', 'bowling', 'cathedrals',
               'billiards', 'monument', 'photo-places', 'informal', 'houses',
               'cafe', 'palace', 'castle', 'health-food', 'anticafe',
               'ice-rink', 'confectioneries', 'bar', 'water-park',
               'slope', 'fitness', 'amusement', 'fastfood', 'vegetarian',
               'gifts', 'bridge', 'homesteads', 'temple', 'square',
               'fountain', 'coffee', 'flea-market', 'diving',
               'karts', 'tea', 'salons', 'climbing-walls', 'church',
               'zoo', 'paintball', 'shooting-ranges', 'monastery',
               'mosque', 'synagogue', 'beaches', 'ozyora', 'rope-park',
               'canteens', 'roof', 'inn', 'pet-store', 'rollerdromes',
               'show-room', 'wind-tunnels', 'stable', 'karaoke']


def prepare_categories(main_array, categories_array_eng, categories_array_rus):
    for index, i in enumerate(main_array):
        for index1, j in enumerate(i):
            for index2, k in enumerate(j):
                if (k['categoriesrus'] == u"Интересные, забавные памятники природы и арх"):
                    main_array[index][index1][index2]['categoriesrus'] = u"Памятники природы"

                if (k['categoriesrus'] == u"Вегетарианские кафе и рестораны"):
                    main_array[index][index1][index2]['categoriesrus'] = u"Вегетарианская еда"

                if (k['categoriesrus'] == u"Тиры и стрелковые клубы"):
                    main_array[index][index1][index2]['categoriesrus'] = u"Тиры"

                if (k['categoriesrus'] == u"Барахолки, блошиные рынки"):
                    main_array[index][index1][index2]['categoriesrus'] = u"Барахолки"

    try:
        categories_array_rus[
            categories_array_rus.index(u"Интересные, забавные памятники природы и арх")] = u"Памятники природы"
    except:
        None

    try:
        categories_array_rus[categories_array_rus.index(u"Вегетарианские кафе и рестораны")] = u"Вегетарианская еда"
    except:
        None

    try:
        categories_array_rus[categories_array_rus.index(u"Тиры и стрелковые клубы ")] = u"Тиры"
    except:
        None

    try:
        categories_array_rus[categories_array_rus.index(u"Барахолки, блошиные рынки")] = u"Барахолки"
    except:
        None

    for i in xrange(len(categories_array_eng)):
        categories_array_eng[i] = categories_array_eng[i].replace('-', '')

    return main_array, categories_array_eng, categories_array_rus
