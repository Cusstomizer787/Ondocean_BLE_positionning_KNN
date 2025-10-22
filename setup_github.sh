#!/bin/bash

echo "🚀 BLE Indoor Positioning KNN - Setup GitHub"
echo "=============================================="
echo ""
echo "📁 Repository: Ondocean_BLE_positionning_KNN"
echo "🔗 URL: https://github.com/Cusstomizer787/Ondocean_BLE_positionning_KNN"
echo "📊 Score: 68/100 - BON"
echo "🎯 Précision: 3.7m erreur moyenne"
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: README.md not found!"
    echo "Please run this script from the Ondocean_BLE_positionning_KNN directory"
    exit 1
fi

echo "✅ Project structure verified"

# Check required files
echo ""
echo "📋 Checking required files..."

files=("README.md" "LICENSE" "requirements.txt" "localize_me.py" "main_qualification.py")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (missing)"
    fi
done

# Check Excel file
if [ -f "Geopos indoor BLE.xlsx" ]; then
    echo "   ✅ Geopos indoor BLE.xlsx ($(stat -f%z Geopos indoor BLE.xlsx) bytes)"
else
    echo "   ❌ Geopos indoor BLE.xlsx (missing - run: python create_excel.py)"
fi

# Check directories
dirs=("src" "data/reference" "docs")
for dir in "${dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "   ✅ $dir/"
    else
        echo "   ❌ $dir/ (missing)"
    fi
done

echo ""
echo "🧪 Testing system..."

# Test Python modules
if python -c "import pandas, numpy, scipy" 2>/dev/null; then
    echo "   ✅ Python dependencies available"
else
    echo "   ⚠️  Install dependencies: pip install -r requirements.txt"
fi

# Test diagnostic
if python diagnostic_simple.py > /dev/null 2>&1; then
    echo "   ✅ System functional"
else
    echo "   ❌ System test failed"
fi

echo ""
echo "📦 Git Repository Setup:"
echo "========================="

echo ""
echo "1. Initialize Git:"
echo "   git init"
echo "   git add ."
echo "   git commit -m \"BLE Indoor Positioning KNN - 3.7m precision system\""
echo ""

echo "2. Create GitHub repository:"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: Ondocean_BLE_positionning_KNN"
echo "   - Description: BLE Indoor Positioning with Fingerprinting KNN (3.7m precision)"
echo "   - Make it public"
echo "   - Don't initialize with README"
echo ""

echo "3. Connect to GitHub:"
echo "   # Replace YOUR_TOKEN with your actual token"
echo "   git remote add origin https://YOUR_TOKEN@github.com/Cusstomizer787/Ondocean_BLE_positionning_KNN.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""

echo "🎯 Usage Instructions:"
echo "===================="
echo ""
echo "📱 Localisation temps réel:"
echo "   python localize_me.py"
echo ""
echo "🔬 Qualification complète:"
echo "   python main_qualification.py"
echo ""
echo "📊 Validation dataset:"
echo "   python diagnostic_simple.py"
echo ""
echo "📝 Exemples:"
echo "   python example_localization.py"
echo ""

echo "📚 Documentation:"
echo "   - README.md (main documentation)"
echo "   - docs/GUIDE_UTILISATION.md (user guide)"
echo "   - docs/RAPPORT_FINAL_COMPARATIF.md (technical report)"
echo ""

echo "🎉 Features:"
echo "   ✅ Fingerprinting KNN (3.7m precision)"
echo "   ✅ 316 measurements dataset"
echo "   ✅ 26 positions training"
echo "   ✅ 5 BLE beacons"
echo "   ✅ Interactive localization"
echo "   ✅ Complete documentation"
echo ""

echo "🏆 Project Status: READY FOR GITHUB!"
echo ""
echo "Next steps:"
echo "1. Create repository on GitHub.com"
echo "2. Run git commands above"
echo "3. Push the code"
echo "4. Share with the world! 🌍"

echo ""
echo "Made with ❤️ for ILEMS 2025"
echo "Author: Nicolas Cusseau"
echo "Method: Fingerprinting KNN (recommended)"
