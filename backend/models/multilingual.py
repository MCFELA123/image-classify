"""
Multilingual Support Module
Provides translations for fruit names and UI text in multiple languages
"""

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Español (Spanish)',
    'fr': 'Français (French)',
    'de': 'Deutsch (German)',
    'zh': '中文 (Chinese)',
    'ja': '日本語 (Japanese)',
    'hi': 'हिन्दी (Hindi)',
    'ar': 'العربية (Arabic)',
    'pt': 'Português (Portuguese)',
    'ru': 'Русский (Russian)'
}

# Fruit name translations
FRUIT_TRANSLATIONS = {
    'Apple': {
        'en': 'Apple',
        'es': 'Manzana',
        'fr': 'Pomme',
        'de': 'Apfel',
        'zh': '苹果',
        'ja': 'りんご',
        'hi': 'सेब',
        'ar': 'تفاحة',
        'pt': 'Maçã',
        'ru': 'Яблоко'
    },
    'Banana': {
        'en': 'Banana',
        'es': 'Plátano',
        'fr': 'Banane',
        'de': 'Banane',
        'zh': '香蕉',
        'ja': 'バナナ',
        'hi': 'केला',
        'ar': 'موز',
        'pt': 'Banana',
        'ru': 'Банан'
    },
    'Orange': {
        'en': 'Orange',
        'es': 'Naranja',
        'fr': 'Orange',
        'de': 'Orange',
        'zh': '橙子',
        'ja': 'オレンジ',
        'hi': 'संतरा',
        'ar': 'برتقال',
        'pt': 'Laranja',
        'ru': 'Апельсин'
    },
    'Mango': {
        'en': 'Mango',
        'es': 'Mango',
        'fr': 'Mangue',
        'de': 'Mango',
        'zh': '芒果',
        'ja': 'マンゴー',
        'hi': 'आम',
        'ar': 'مانجو',
        'pt': 'Manga',
        'ru': 'Манго'
    },
    'Strawberry': {
        'en': 'Strawberry',
        'es': 'Fresa',
        'fr': 'Fraise',
        'de': 'Erdbeere',
        'zh': '草莓',
        'ja': 'いちご',
        'hi': 'स्ट्रॉबेरी',
        'ar': 'فراولة',
        'pt': 'Morango',
        'ru': 'Клубника'
    },
    'Grape': {
        'en': 'Grape',
        'es': 'Uva',
        'fr': 'Raisin',
        'de': 'Traube',
        'zh': '葡萄',
        'ja': 'ぶどう',
        'hi': 'अंगूर',
        'ar': 'عنب',
        'pt': 'Uva',
        'ru': 'Виноград'
    },
    'Watermelon': {
        'en': 'Watermelon',
        'es': 'Sandía',
        'fr': 'Pastèque',
        'de': 'Wassermelone',
        'zh': '西瓜',
        'ja': 'スイカ',
        'hi': 'तरबूज',
        'ar': 'بطيخ',
        'pt': 'Melancia',
        'ru': 'Арбуз'
    },
    'Pineapple': {
        'en': 'Pineapple',
        'es': 'Piña',
        'fr': 'Ananas',
        'de': 'Ananas',
        'zh': '菠萝',
        'ja': 'パイナップル',
        'hi': 'अनानास',
        'ar': 'أناناس',
        'pt': 'Abacaxi',
        'ru': 'Ананас'
    },
    'Cherry': {
        'en': 'Cherry',
        'es': 'Cereza',
        'fr': 'Cerise',
        'de': 'Kirsche',
        'zh': '樱桃',
        'ja': 'さくらんぼ',
        'hi': 'चेरी',
        'ar': 'كرز',
        'pt': 'Cereja',
        'ru': 'Вишня'
    },
    'Kiwi': {
        'en': 'Kiwi',
        'es': 'Kiwi',
        'fr': 'Kiwi',
        'de': 'Kiwi',
        'zh': '猕猴桃',
        'ja': 'キウイ',
        'hi': 'कीवी',
        'ar': 'كيوي',
        'pt': 'Kiwi',
        'ru': 'Киви'
    }
}

# UI Text translations
UI_TRANSLATIONS = {
    'title': {
        'en': 'Fruit Classification System',
        'es': 'Sistema de Clasificación de Frutas',
        'fr': 'Système de Classification des Fruits',
        'de': 'Fruchtklassifizierungssystem',
        'zh': '水果分类系统',
        'ja': '果物分類システム',
        'hi': 'फल वर्गीकरण प्रणाली',
        'ar': 'نظام تصنيف الفواكه',
        'pt': 'Sistema de Classificação de Frutas',
        'ru': 'Система Классификации Фруктов'
    },
    'classify': {
        'en': 'Classify',
        'es': 'Clasificar',
        'fr': 'Classifier',
        'de': 'Klassifizieren',
        'zh': '分类',
        'ja': '分類',
        'hi': 'वर्गीकृत करें',
        'ar': 'تصنيف',
        'pt': 'Classificar',
        'ru': 'Классифицировать'
    },
    'history': {
        'en': 'History',
        'es': 'Historial',
        'fr': 'Historique',
        'de': 'Verlauf',
        'zh': '历史记录',
        'ja': '履歴',
        'hi': 'इतिहास',
        'ar': 'السجل',
        'pt': 'Histórico',
        'ru': 'История'
    },
    'statistics': {
        'en': 'Statistics',
        'es': 'Estadísticas',
        'fr': 'Statistiques',
        'de': 'Statistiken',
        'zh': '统计数据',
        'ja': '統計',
        'hi': 'आँकड़े',
        'ar': 'إحصائيات',
        'pt': 'Estatísticas',
        'ru': 'Статистика'
    },
    'upload_image': {
        'en': 'Upload Image',
        'es': 'Subir Imagen',
        'fr': 'Télécharger l\'image',
        'de': 'Bild hochladen',
        'zh': '上传图片',
        'ja': '画像をアップロード',
        'hi': 'चित्र अपलोड करें',
        'ar': 'تحميل الصورة',
        'pt': 'Carregar Imagem',
        'ru': 'Загрузить изображение'
    },
    'confidence': {
        'en': 'Confidence',
        'es': 'Confianza',
        'fr': 'Confiance',
        'de': 'Vertrauen',
        'zh': '置信度',
        'ja': '信頼度',
        'hi': 'विश्वास',
        'ar': 'الثقة',
        'pt': 'Confiança',
        'ru': 'Уверенность'
    },
    'ripeness': {
        'en': 'Ripeness',
        'es': 'Madurez',
        'fr': 'Maturité',
        'de': 'Reife',
        'zh': '成熟度',
        'ja': '熟度',
        'hi': 'पकापन',
        'ar': 'النضج',
        'pt': 'Maturação',
        'ru': 'Зрелость'
    },
    'quality': {
        'en': 'Quality',
        'es': 'Calidad',
        'fr': 'Qualité',
        'de': 'Qualität',
        'zh': '质量',
        'ja': '品質',
        'hi': 'गुणवत्ता',
        'ar': 'الجودة',
        'pt': 'Qualidade',
        'ru': 'Качество'
    },
    'size_grade': {
        'en': 'Size Grade',
        'es': 'Grado de Tamaño',
        'fr': 'Grade de Taille',
        'de': 'Größenklasse',
        'zh': '大小等级',
        'ja': 'サイズ等級',
        'hi': 'आकार ग्रेड',
        'ar': 'درجة الحجم',
        'pt': 'Grau de Tamanho',
        'ru': 'Размерный класс'
    },
    'nutrition': {
        'en': 'Nutrition',
        'es': 'Nutrición',
        'fr': 'Nutrition',
        'de': 'Ernährung',
        'zh': '营养',
        'ja': '栄養',
        'hi': 'पोषण',
        'ar': 'التغذية',
        'pt': 'Nutrição',
        'ru': 'Питание'
    },
    'unripe': {
        'en': 'Unripe',
        'es': 'Verde/Inmaduro',
        'fr': 'Non mûr',
        'de': 'Unreif',
        'zh': '未成熟',
        'ja': '未熟',
        'hi': 'कच्चा',
        'ar': 'غير ناضج',
        'pt': 'Verde',
        'ru': 'Незрелый'
    },
    'ripe': {
        'en': 'Ripe',
        'es': 'Maduro',
        'fr': 'Mûr',
        'de': 'Reif',
        'zh': '成熟',
        'ja': '熟した',
        'hi': 'पका हुआ',
        'ar': 'ناضج',
        'pt': 'Maduro',
        'ru': 'Зрелый'
    },
    'overripe': {
        'en': 'Overripe',
        'es': 'Demasiado maduro',
        'fr': 'Trop mûr',
        'de': 'Überreif',
        'zh': '过熟',
        'ja': '熟し過ぎ',
        'hi': 'अधिक पका',
        'ar': 'مفرط النضج',
        'pt': 'Muito maduro',
        'ru': 'Перезрелый'
    },
    'healthy': {
        'en': 'Healthy',
        'es': 'Saludable',
        'fr': 'Sain',
        'de': 'Gesund',
        'zh': '健康',
        'ja': '健康',
        'hi': 'स्वस्थ',
        'ar': 'صحي',
        'pt': 'Saudável',
        'ru': 'Здоровый'
    },
    'defective': {
        'en': 'Defective',
        'es': 'Defectuoso',
        'fr': 'Défectueux',
        'de': 'Beschädigt',
        'zh': '有缺陷',
        'ja': '欠陥あり',
        'hi': 'दोषपूर्ण',
        'ar': 'معيب',
        'pt': 'Defeituoso',
        'ru': 'Дефектный'
    },
    'small': {
        'en': 'Small',
        'es': 'Pequeño',
        'fr': 'Petit',
        'de': 'Klein',
        'zh': '小',
        'ja': '小',
        'hi': 'छोटा',
        'ar': 'صغير',
        'pt': 'Pequeno',
        'ru': 'Маленький'
    },
    'medium': {
        'en': 'Medium',
        'es': 'Mediano',
        'fr': 'Moyen',
        'de': 'Mittel',
        'zh': '中',
        'ja': '中',
        'hi': 'मध्यम',
        'ar': 'متوسط',
        'pt': 'Médio',
        'ru': 'Средний'
    },
    'large': {
        'en': 'Large',
        'es': 'Grande',
        'fr': 'Grand',
        'de': 'Groß',
        'zh': '大',
        'ja': '大',
        'hi': 'बड़ा',
        'ar': 'كبير',
        'pt': 'Grande',
        'ru': 'Большой'
    },
    'calories': {
        'en': 'Calories',
        'es': 'Calorías',
        'fr': 'Calories',
        'de': 'Kalorien',
        'zh': '卡路里',
        'ja': 'カロリー',
        'hi': 'कैलोरी',
        'ar': 'السعرات الحرارية',
        'pt': 'Calorias',
        'ru': 'Калории'
    },
    'vitamins': {
        'en': 'Vitamins',
        'es': 'Vitaminas',
        'fr': 'Vitamines',
        'de': 'Vitamine',
        'zh': '维生素',
        'ja': 'ビタミン',
        'hi': 'विटामिन',
        'ar': 'الفيتامينات',
        'pt': 'Vitaminas',
        'ru': 'Витамины'
    },
    'health_benefits': {
        'en': 'Health Benefits',
        'es': 'Beneficios para la Salud',
        'fr': 'Bienfaits pour la Santé',
        'de': 'Gesundheitsvorteile',
        'zh': '健康益处',
        'ja': '健康効果',
        'hi': 'स्वास्थ्य लाभ',
        'ar': 'الفوائد الصحية',
        'pt': 'Benefícios para a Saúde',
        'ru': 'Польза для здоровья'
    }
}


def get_fruit_name(fruit_class, language='en'):
    """
    Get fruit name in specified language
    
    Args:
        fruit_class: English name of the fruit
        language: Language code (default: 'en')
        
    Returns:
        Translated fruit name
    """
    if fruit_class in FRUIT_TRANSLATIONS:
        translations = FRUIT_TRANSLATIONS[fruit_class]
        return translations.get(language, translations.get('en', fruit_class))
    return fruit_class


def get_ui_text(key, language='en'):
    """
    Get UI text in specified language
    
    Args:
        key: Translation key
        language: Language code (default: 'en')
        
    Returns:
        Translated text
    """
    if key in UI_TRANSLATIONS:
        translations = UI_TRANSLATIONS[key]
        return translations.get(language, translations.get('en', key))
    return key


def get_supported_languages():
    """Get list of supported languages"""
    return SUPPORTED_LANGUAGES


def translate_result(result_dict, language='en'):
    """
    Translate all translatable fields in a result dictionary
    
    Args:
        result_dict: Dictionary containing classification results
        language: Target language code
        
    Returns:
        Dictionary with translated fields
    """
    translated = result_dict.copy()
    
    # Translate fruit class
    if 'predicted_class' in translated:
        translated['predicted_class_translated'] = get_fruit_name(
            translated['predicted_class'], language
        )
    
    # Translate ripeness
    if 'ripeness' in translated:
        ripeness_key = translated['ripeness'].lower()
        translated['ripeness_translated'] = get_ui_text(ripeness_key, language)
    
    # Translate quality
    if 'quality_status' in translated:
        quality_key = translated['quality_status'].lower()
        translated['quality_status_translated'] = get_ui_text(quality_key, language)
    
    # Translate size grade
    if 'size_grade' in translated:
        size_key = translated['size_grade'].lower()
        translated['size_grade_translated'] = get_ui_text(size_key, language)
    
    return translated
