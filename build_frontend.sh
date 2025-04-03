cd projection_mapping_source
npm install
npm run build

rm -rf ../projection_mapping
cp -r build ../projection_mapping
rm -rf build
