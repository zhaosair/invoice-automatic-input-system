pip install --user numpy scipy matplotlib pillow
pip install --user easydict opencv-python keras h5py PyYAML
pip install --user cython==0.24

# for gpu
# pip install tensorflow-gpu==1.3.0
# chmod +x ./ctpn/lib/utils/make.sh
# cd ./ctpn/lib/utils/ && ./make.sh

# for cpu
pip install --user tensorflow==1.3.0
chmod +x ./ctpn/lib/utils/make_cpu.sh
cd ./ctpn/lib/utils/ && ./make_cpu.sh
