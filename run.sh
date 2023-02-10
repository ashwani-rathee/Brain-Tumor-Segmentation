cd vectorization_server
echo "Starting vectorization server"
npm run start &

cd ..
cd segment_server
echo "Starting segmentation server"
python3 app.py &