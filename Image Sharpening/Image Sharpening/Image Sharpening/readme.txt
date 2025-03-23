操作方法:
(有matplotlib的函式庫可呈現圖像視覺化方便觀察)

直接使用python3 main.py 或是 python main.py (約10-20秒左右)即可秀出結果

-----------------------------------------------------------------------------------------------------
流程:
1.利用Image.open將兩種圖片讀入，並用convert('L')將圖片轉成灰階
2.設定laplacian_filter
3.將圖片進行laplacian運算，主要是利用for迴圈將矩陣的每個點進行計算:
val = np.sum(laplacian_filter*image[i-1:i+2,j-1:j+2])
image_result[i,j] = np.clip(val, 0, 255)
用val先將結果儲存再用np.clip避免overflow的問題產生。
4.將圖片進行high_boost運算
np.array([[0, -1, 0], [-1, 4+k, -1], [0, -1, 0]])，其中k是可變參數，這裡設定為2.7。
並同樣用
sharp = np.clip(image + laplacian, 0, 255).astype(np.uint8)
並免overflow的問題產生

5.最後印出原圖、laplacian運算、high_boost運算後的結果