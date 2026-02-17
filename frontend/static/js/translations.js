// UI Translations for all supported languages
const TRANSLATIONS = {
    // Navigation
    'nav.classify': {
        en: 'Classify', es: 'Clasificar', fr: 'Classifier', de: 'Klassifizieren',
        zh: '分类', ja: '分類', hi: 'वर्गीकृत करें', pt: 'Classificar'
    },
    'nav.webcam': {
        en: 'Webcam', es: 'Cámara', fr: 'Caméra', de: 'Webcam',
        zh: '摄像头', ja: 'ウェブカメラ', hi: 'वेबकैम', pt: 'Webcam'
    },
    'nav.dashboard': {
        en: 'Dashboard', es: 'Panel', fr: 'Tableau de bord', de: 'Dashboard',
        zh: '仪表板', ja: 'ダッシュボード', hi: 'डैशबोर्ड', pt: 'Painel'
    },
    'nav.nutrition': {
        en: 'Nutrition', es: 'Nutrición', fr: 'Nutrition', de: 'Ernährung',
        zh: '营养', ja: '栄養', hi: 'पोषण', pt: 'Nutrição'
    },
    'nav.inventory': {
        en: 'Inventory', es: 'Inventario', fr: 'Inventaire', de: 'Inventar',
        zh: '库存', ja: '在庫', hi: 'इन्वेंटरी', pt: 'Inventário'
    },
    'nav.history': {
        en: 'History', es: 'Historial', fr: 'Historique', de: 'Verlauf',
        zh: '历史', ja: '履歴', hi: 'इतिहास', pt: 'Histórico'
    },

    // Header
    'header.title': {
        en: 'Fruit Classification System', es: 'Sistema de Clasificación de Frutas',
        fr: 'Système de Classification des Fruits', de: 'Fruchtklassifizierungssystem',
        zh: '水果分类系统', ja: '果物分類システム', hi: 'फल वर्गीकरण प्रणाली', pt: 'Sistema de Classificação de Frutas'
    },
    'header.login': {
        en: 'Login', es: 'Iniciar Sesión', fr: 'Connexion', de: 'Anmelden',
        zh: '登录', ja: 'ログイン', hi: 'लॉग इन', pt: 'Entrar'
    },

    // Classify Section
    'classify.title': {
        en: 'Upload & Analyze', es: 'Subir y Analizar', fr: 'Télécharger et Analyser', de: 'Hochladen und Analysieren',
        zh: '上传并分析', ja: 'アップロードして分析', hi: 'अपलोड और विश्लेषण करें', pt: 'Carregar e Analisar'
    },
    'classify.dropzone': {
        en: 'Drop fruit image here or click to upload', es: 'Suelta la imagen de la fruta aquí o haz clic para subir',
        fr: 'Déposez l\'image du fruit ici ou cliquez pour télécharger', de: 'Fruchtbild hier ablegen oder klicken zum Hochladen',
        zh: '将水果图片拖放到此处或点击上传', ja: '果物の画像をここにドロップするか、クリックしてアップロード',
        hi: 'फल की छवि यहाँ छोड़ें या अपलोड करने के लिए क्लिक करें', pt: 'Solte a imagem da fruta aqui ou clique para carregar'
    },
    'classify.formats': {
        en: 'Supports: JPG, PNG, GIF, WebP (Max 16MB)', es: 'Soporta: JPG, PNG, GIF, WebP (Máx 16MB)',
        fr: 'Formats: JPG, PNG, GIF, WebP (Max 16Mo)', de: 'Unterstützt: JPG, PNG, GIF, WebP (Max 16MB)',
        zh: '支持: JPG, PNG, GIF, WebP (最大16MB)', ja: '対応形式: JPG, PNG, GIF, WebP (最大16MB)',
        hi: 'समर्थित: JPG, PNG, GIF, WebP (अधिकतम 16MB)', pt: 'Suporta: JPG, PNG, GIF, WebP (Máx 16MB)'
    },
    'classify.button': {
        en: 'Analyze Fruit', es: 'Analizar Fruta', fr: 'Analyser le Fruit', de: 'Frucht Analysieren',
        zh: '分析水果', ja: '果物を分析', hi: 'फल का विश्लेषण करें', pt: 'Analisar Fruta'
    },
    'classify.takePhoto': {
        en: 'Take Photo', es: 'Tomar Foto', fr: 'Prendre une Photo', de: 'Foto Aufnehmen',
        zh: '拍照', ja: '写真を撮る', hi: 'फोटो लें', pt: 'Tirar Foto'
    },

    // Results
    'results.title': {
        en: 'Analysis Results', es: 'Resultados del Análisis', fr: 'Résultats de l\'Analyse', de: 'Analyseergebnisse',
        zh: '分析结果', ja: '分析結果', hi: 'विश्लेषण परिणाम', pt: 'Resultados da Análise'
    },
    'results.confidence': {
        en: 'Confidence', es: 'Confianza', fr: 'Confiance', de: 'Vertrauen',
        zh: '置信度', ja: '信頼度', hi: 'विश्वास', pt: 'Confiança'
    },
    'results.topPredictions': {
        en: 'Top Predictions', es: 'Principales Predicciones', fr: 'Meilleures Prédictions', de: 'Top Vorhersagen',
        zh: '最佳预测', ja: 'トップ予測', hi: 'शीर्ष भविष्यवाणियां', pt: 'Principais Previsões'
    },
    'results.ripeness': {
        en: 'Ripeness', es: 'Madurez', fr: 'Maturité', de: 'Reife',
        zh: '成熟度', ja: '熟度', hi: 'पकापन', pt: 'Maturação'
    },
    'results.quality': {
        en: 'Quality', es: 'Calidad', fr: 'Qualité', de: 'Qualität',
        zh: '质量', ja: '品質', hi: 'गुणवत्ता', pt: 'Qualidade'
    },
    'results.qualityScore': {
        en: 'Quality Score', es: 'Puntuación de Calidad', fr: 'Score de Qualité', de: 'Qualitätsbewertung',
        zh: '质量评分', ja: '品質スコア', hi: 'गुणवत्ता स्कोर', pt: 'Pontuação de Qualidade'
    },
    'results.edible': {
        en: 'Edible', es: 'Comestible', fr: 'Comestible', de: 'Essbar',
        zh: '可食用', ja: '食用可', hi: 'खाने योग्य', pt: 'Comestível'
    },
    'results.defects': {
        en: 'Defects Detected', es: 'Defectos Detectados', fr: 'Défauts Détectés', de: 'Erkannte Mängel',
        zh: '检测到的缺陷', ja: '検出された欠陥', hi: 'पता लगाए गए दोष', pt: 'Defeitos Detectados'
    },
    'results.size': {
        en: 'Size', es: 'Tamaño', fr: 'Taille', de: 'Größe',
        zh: '大小', ja: 'サイズ', hi: 'आकार', pt: 'Tamanho'
    },
    'results.grade': {
        en: 'Grade', es: 'Grado', fr: 'Grade', de: 'Klasse',
        zh: '等级', ja: 'グレード', hi: 'ग्रेड', pt: 'Nota'
    },
    'results.suitableFor': {
        en: 'Suitable For', es: 'Adecuado Para', fr: 'Adapté Pour', de: 'Geeignet Für',
        zh: '适用于', ja: '適用用途', hi: 'के लिए उपयुक्त', pt: 'Adequado Para'
    },

    // Nutrition
    'nutrition.title': {
        en: 'Nutritional Information', es: 'Información Nutricional', fr: 'Informations Nutritionnelles', de: 'Nährwertinformationen',
        zh: '营养信息', ja: '栄養情報', hi: 'पोषण संबंधी जानकारी', pt: 'Informação Nutricional'
    },
    'nutrition.calories': {
        en: 'Calories', es: 'Calorías', fr: 'Calories', de: 'Kalorien',
        zh: '卡路里', ja: 'カロリー', hi: 'कैलोरी', pt: 'Calorias'
    },
    'nutrition.carbs': {
        en: 'Carbohydrates', es: 'Carbohidratos', fr: 'Glucides', de: 'Kohlenhydrate',
        zh: '碳水化合物', ja: '炭水化物', hi: 'कार्बोहाइड्रेट', pt: 'Carboidratos'
    },
    'nutrition.fiber': {
        en: 'Fiber', es: 'Fibra', fr: 'Fibres', de: 'Ballaststoffe',
        zh: '纤维', ja: '食物繊維', hi: 'फाइबर', pt: 'Fibra'
    },
    'nutrition.sugar': {
        en: 'Sugar', es: 'Azúcar', fr: 'Sucre', de: 'Zucker',
        zh: '糖', ja: '糖分', hi: 'चीनी', pt: 'Açúcar'
    },
    'nutrition.protein': {
        en: 'Protein', es: 'Proteína', fr: 'Protéines', de: 'Protein',
        zh: '蛋白质', ja: 'タンパク質', hi: 'प्रोटीन', pt: 'Proteína'
    },
    'nutrition.vitamins': {
        en: 'Vitamins', es: 'Vitaminas', fr: 'Vitamines', de: 'Vitamine',
        zh: '维生素', ja: 'ビタミン', hi: 'विटामिन', pt: 'Vitaminas'
    },
    'nutrition.healthBenefits': {
        en: 'Health Benefits', es: 'Beneficios para la Salud', fr: 'Bienfaits pour la Santé', de: 'Gesundheitsvorteile',
        zh: '健康益处', ja: '健康効果', hi: 'स्वास्थ्य लाभ', pt: 'Benefícios para a Saúde'
    },
    'nutrition.browse': {
        en: 'Browse Nutrition Database', es: 'Explorar Base de Datos Nutricional', fr: 'Parcourir la Base de Données Nutritionnelle', de: 'Nährwertdatenbank Durchsuchen',
        zh: '浏览营养数据库', ja: '栄養データベースを閲覧', hi: 'पोषण डेटाबेस ब्राउज़ करें', pt: 'Navegar Banco de Dados Nutricional'
    },

    // Webcam
    'webcam.title': {
        en: 'Real-Time Detection', es: 'Detección en Tiempo Real', fr: 'Détection en Temps Réel', de: 'Echtzeit-Erkennung',
        zh: '实时检测', ja: 'リアルタイム検出', hi: 'रीयल-टाइम डिटेक्शन', pt: 'Detecção em Tempo Real'
    },
    'webcam.start': {
        en: 'Start Camera', es: 'Iniciar Cámara', fr: 'Démarrer Caméra', de: 'Kamera Starten',
        zh: '启动摄像头', ja: 'カメラを開始', hi: 'कैमरा शुरू करें', pt: 'Iniciar Câmera'
    },
    'webcam.stop': {
        en: 'Stop Camera', es: 'Detener Cámara', fr: 'Arrêter Caméra', de: 'Kamera Stoppen',
        zh: '停止摄像头', ja: 'カメラを停止', hi: 'कैमरा बंद करें', pt: 'Parar Câmera'
    },
    'webcam.capture': {
        en: 'Capture & Analyze', es: 'Capturar y Analizar', fr: 'Capturer et Analyser', de: 'Aufnehmen und Analysieren',
        zh: '捕获并分析', ja: 'キャプチャして分析', hi: 'कैप्चर और विश्लेषण करें', pt: 'Capturar e Analisar'
    },

    // Dashboard
    'dashboard.title': {
        en: 'Analytics Dashboard', es: 'Panel de Análisis', fr: 'Tableau de Bord Analytique', de: 'Analyse-Dashboard',
        zh: '分析仪表板', ja: '分析ダッシュボード', hi: 'एनालिटिक्स डैशबोर्ड', pt: 'Painel Analítico'
    },
    'dashboard.refresh': {
        en: 'Refresh', es: 'Actualizar', fr: 'Actualiser', de: 'Aktualisieren',
        zh: '刷新', ja: '更新', hi: 'रिफ्रेश करें', pt: 'Atualizar'
    },
    'dashboard.totalClassifications': {
        en: 'Total Classifications', es: 'Clasificaciones Totales', fr: 'Classifications Totales', de: 'Gesamtklassifikationen',
        zh: '总分类数', ja: '総分類数', hi: 'कुल वर्गीकरण', pt: 'Total de Classificações'
    },

    // History
    'history.title': {
        en: 'Classification History', es: 'Historial de Clasificación', fr: 'Historique des Classifications', de: 'Klassifizierungsverlauf',
        zh: '分类历史', ja: '分類履歴', hi: 'वर्गीकरण इतिहास', pt: 'Histórico de Classificação'
    },
    'history.refresh': {
        en: 'Refresh', es: 'Actualizar', fr: 'Actualiser', de: 'Aktualisieren',
        zh: '刷新', ja: '更新', hi: 'रिफ्रेश करें', pt: 'Atualizar'
    },
    'history.noRecords': {
        en: 'No classification history yet', es: 'Aún no hay historial de clasificación', fr: 'Pas encore d\'historique de classification', de: 'Noch keine Klassifizierungshistorie',
        zh: '暂无分类历史', ja: 'まだ分類履歴がありません', hi: 'अभी तक कोई वर्गीकरण इतिहास नहीं', pt: 'Ainda não há histórico de classificação'
    },

    // Inventory
    'inventory.title': {
        en: 'Inventory Management', es: 'Gestión de Inventario', fr: 'Gestion des Stocks', de: 'Bestandsverwaltung',
        zh: '库存管理', ja: '在庫管理', hi: 'इन्वेंटरी प्रबंधन', pt: 'Gestão de Inventário'
    },
    'inventory.generateQR': {
        en: 'Generate QR', es: 'Generar QR', fr: 'Générer QR', de: 'QR Generieren',
        zh: '生成二维码', ja: 'QR生成', hi: 'QR जेनरेट करें', pt: 'Gerar QR'
    },
    'inventory.refresh': {
        en: 'Refresh', es: 'Actualizar', fr: 'Actualiser', de: 'Aktualisieren',
        zh: '刷新', ja: '更新', hi: 'रिफ्रेश करें', pt: 'Atualizar'
    },

    // Common
    'common.loading': {
        en: 'Loading...', es: 'Cargando...', fr: 'Chargement...', de: 'Wird geladen...',
        zh: '加载中...', ja: '読み込み中...', hi: 'लोड हो रहा है...', pt: 'Carregando...'
    },
    'common.error': {
        en: 'Error', es: 'Error', fr: 'Erreur', de: 'Fehler',
        zh: '错误', ja: 'エラー', hi: 'त्रुटि', pt: 'Erro'
    },
    'common.success': {
        en: 'Success', es: 'Éxito', fr: 'Succès', de: 'Erfolg',
        zh: '成功', ja: '成功', hi: 'सफलता', pt: 'Sucesso'
    },
    'common.yes': {
        en: 'Yes', es: 'Sí', fr: 'Oui', de: 'Ja',
        zh: '是', ja: 'はい', hi: 'हाँ', pt: 'Sim'
    },
    'common.no': {
        en: 'No', es: 'No', fr: 'Non', de: 'Nein',
        zh: '否', ja: 'いいえ', hi: 'नहीं', pt: 'Não'
    }
};

// Function to get translation
function t(key, lang = null) {
    const language = lang || currentLanguage || 'en';
    if (TRANSLATIONS[key] && TRANSLATIONS[key][language]) {
        return TRANSLATIONS[key][language];
    }
    // Fallback to English
    if (TRANSLATIONS[key] && TRANSLATIONS[key]['en']) {
        return TRANSLATIONS[key]['en'];
    }
    console.warn(`Translation missing for key: ${key}`);
    return key;
}

// Function to update all UI text
function updateUILanguage() {
    console.log('Updating UI to language:', currentLanguage);
    
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const translation = t(key);
        if (translation !== key) {
            el.textContent = translation;
        }
    });
    
    // Update placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        el.placeholder = t(key);
    });
    
    // Update title attributes
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const key = el.getAttribute('data-i18n-title');
        el.title = t(key);
    });
    
    console.log('UI language update complete');
}
