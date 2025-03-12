# How to architect and build an End-to-End AWS Web Application 

**Video Demo:** [Watch the deployment walkthrough](https://www.youtube.com/watch?v=7m_q1ldzw0U&t=327s)

- **AIM**: the project aims to train and enhance the knowledge about AWS service. I followed the video which Youtuber, named “Tiny Technical Tutorials”, teach how to set up the web application.

### **What do we need**
---
1. A way to create/host a webpage
2. A way to invoke the math functionality
3. A way to do some math
4. Somewhere to store/return the math result

### **What do you need:**
---
1. A text editer (Notepad++)
2. An AWS account
3. Basic knowledge of AWS

## Step1. AWS Amplify

AWS Amplify 是 Amazon Web Services（AWS）提供的一組工具和服務，用於快速開發、部署及管理雲端應用程式，特別適合前端與行動應用開發。它可以讓開發者更輕鬆地將應用程式與 AWS 的後端服務（如認證、資料存儲、API）整合，並且支援 React、Vue、Angular、Next.js、Flutter、iOS 和 Android 等框架與平台。

在 Amplify 主控台中選擇 "Deploy without Git" 選項時，您需要先準備好前端檔案，包括：

- HTML 文件：定義網頁結構
    - ( 請注意：如果開不起來，有部分問題可能在於你需要將檔名改成 index.html，如此才能打開建立好的網址，並且.zip檔案中需要直接把所有的檔案打工放在一起）
- CSS 文件：設定網頁樣式
- JavaScript 文件：實現網頁功能和互動

這些檔案可以直接上傳到 Amplify，系統會自動處理部署流程，為您的應用程式建立一個可訪問的 URL。

### Step 2. AWS lambda

AWS Lambda 是一個無伺服器運算平台，讓開發人員能夠執行程式碼而無需管理伺服器。它採用事件驅動的方式運作，只在需要時才執行程式碼，並根據使用量自動調整運算資源。

- 主要特點包括：
    - 自動擴展：根據工作負載自動調整資源，無需手動配置
    - 按需付費：只需為實際執行的程式碼時間付費，閒置時不產生費用
    - 支援多種程式語言：包括 Python、Node.js、Java、C# 等
    - 與其他 AWS 服務完美整合：可輕鬆連接 API Gateway、S3、DynamoDB 等服務
- Lambda 函數特別適合用於：
    - 處理 API 請求
    - 自動化數據處理
    - 即時檔案處理
    - 排程任務執行

### Step3. AWS API

<aside>
AWS API Gateway 是一項完全受管理的服務，可讓開發人員建立、發布、維護、監控和保護任何規模的 API。它作為應用程式的「前門」，允許應用程式存取後端服務的資料、商業邏輯或功能。

API Gateway 的主要功能包括：

- 處理所有 API 呼叫的任務，包括流量管理、授權和存取控制、監控以及 API 版本管理
- 支援 RESTful API 和 WebSocket API
- 與其他 AWS 服務（如 Lambda、EC2）無縫整合
- 提供強大的安全功能，包括 AWS IAM 整合和 API 金鑰管理
</aside>

- 設定API
    1. Create API
    2. setting API type (in this case, we choose REST API) 
    3. naming this API and create a new one
- 設定連結API的方式（Create Method)
    1. Setting ‘method type’ (in this case, POST method) 
        - Method type
            1. 定義了用戶端可以對 API 資源執行的操作。
            2. 允許您根據不同的操作配置不同的請求和響應處理。
            3. 有助於設計符合 RESTful API 原則的 API。
            - **GET：**
                - 用於檢索資源。
                - 通常不應修改伺服器上的資料。
                - 例如：獲取使用者資訊、檢索產品列表。
            - **POST：**
                - 用於提交資料以創建新資源。
                - 例如：創建新使用者、提交訂單。
            - **PUT：**
                - 用於更新現有資源。
                - 通常用於替換整個資源。
                - 例如：更新使用者資訊、替換產品詳細資訊。
            - **PATCH：**
                - 用於對現有資源進行部分修改。
                - 通常用於更新資源的特定欄位。
                - 例如：更新使用者名稱、修改產品價格。
            - **DELETE：**
                - 用於刪除資源。
                - 例如：刪除使用者、移除產品。
            - **HEAD：**
                - 與GET方法相同，但僅返回HTTP標頭，不返回響應主體。
                - 用於檢查資源是否存在或獲取資源的元數據。
            - **OPTIONS：**
                - 用於獲取伺服器支持的HTTP方法。
                - 通常用於CORS（跨來源資源共享）預檢請求。
            - **ANY：**
                - 代表要在執行階段提供的任何HTTP方法。
                - 這允許您使用單個API Gateway資源處理所有HTTP方法。
    2. Integration type: lambda 
        
        > Don’t forget to click ‘**Lambda proxy integration’.**
        > 
        - 為什麼需要點擊那個？
            - 在資料傳輸過程中，Lambda 設定的程式主要是以 event 為主。如果只是單純點選而不啟用 Lambda proxy integration，函數將無法在物件中找到 body（主體）。主體就像一個容器，它需要將所有必要的數值打包在裡面，以便在 HTTP 請求（以JSON形式）中傳輸資料。
            - APIgateway 有不同整合方式，用於將前端請求送到後端，包括：
                - **Lambda 代理整合 (Lambda Proxy Integration)：**
                    - 這種整合類型將完整的 HTTP 請求（包含 headers、body、query string 等）以 JSON 事件物件的形式傳送給 Lambda 函數。
                    - Lambda 函數必須解析此事件物件以取得請求的詳細內容。
                    - 此整合類型的優點在於它簡化了 API Gateway 的設定流程，同時讓 Lambda 函數能夠處理多種請求類型。
                - **AWS 服務整合 (AWS Service Integration)：**
                    - 此整合類型讓您能夠將 API Gateway 直接連接至其他 AWS 服務，如 DynamoDB、S3 等。
                    - 您可以自行將請求參數對應至 AWS 服務所需的格式。
                    - 此方式特別適合與特定 AWS 服務進行互動。
            
    3. Select the lambda function
    4. make sure “Request Validator” is Validate body
        - 確保請求的格式以及內容中有包含body，避免出現問題
- 點擊 “ Enable CORC(CORS (Cross-Origin Resource Sharing)” → 保護使用者安全同時確保跨網域的請求是安全的
    - 選擇需要連結的方式
    - 限制 Origin的網址
- 測試API （直接輸入數值即可）
- 現在，你已經將APIgateway 連結到 Lambda （但還沒有到前端喔）

### Step4. AWS DynamoDB

<aside>
AWS DynamoDB 是一個完全託管的 NoSQL 資料庫服務，提供快速且可預測的效能。它特別適合需要高效能和可擴展性的應用程式，並且完全整合於 AWS 生態系統中。

</aside>

1. 創建 DynamoDB
2. 設定 primary key 
3. 複製 ARN (Amazon Resource Name)  → 稍後會用到IAM上，確保 lambda 是有權限可以連接到 DynamoDB

### Step5. IAM

To ensure the lambda have access to connect DynamoDB. 

1. 打開 lambda
2. 點選 “Configuration” → 點選 Execution role 中的URL 
3. 導向 IAM, 設定 JSON policy. 
4. 同時在 Resource上加上 DynamoDB的ARN

### Step6. 修改Lambda

加入程式碼已便讓資料可以導入到DynamoDB 

記得有哪些input(e.g., id, num1, num2, operator, and result etc.) 需要寫入database.

可以使用TEST 來檢查看看是不是有寫入 DynamoDB.

### Step7. 將前端利用API 進行連結

- 修改前端已提供與API連結的管道

### Final: 可以測試看看有沒有問題， 有問題就請問cahtGPT
