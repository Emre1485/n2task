# N2Mobil Backend Task

## 1. Projede Kullanılan Teknolojiler

* **Backend:** Python, Django, DRF
* **Veritabanı:** PostgreSQL
* **Cache:** Redis
* **Containerization:** Docker
* **Dökümantasyon:** Swagger UI

## 2. Kurulum ve Çalıştırma

### 2.1. Docker ile Çalıştırma

Projeyi Docker ile ayağa kaldırmak için:

1. Projeyi klonlayın.
2. Terminali proje dizininde açın.
3. Aşağıdaki komutu çalıştırın:
```shell
docker-compose up --build
```

Bu komut Web, DB ve Redis servislerini başlatacaktır.

Tarayıcıdan
```shell
http://localhost:8000/swagger/
``` 
adresine giderek API dökümantasyonuna erişebilir ve endpoint'leri test edebilirsiniz.

### 2.2. Lokal Çalıştırma

Lokal çalıştırma için makinenizde PostgreSQL ve Redis'in kurulu olması gerekmektedir.

1. Yeni bir Virtual Environment oluşturun ve aktif edin.
2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```
3. `manage.py` ile aynı dizinde **`.env`** dosyası oluşturun ve aşağıdaki ayarları kendinize göre düzenleyin:
```bash
SECRET_KEY='gizli key'
DEBUG=True
DB_NAME=taskdb
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://127.0.0.1:6379/1
```
4. Veritabanı tablolarını oluşturun (Migrate):
```bash
python manage.py migrate
```
5. Sunucuyu başlatın:
```bash
python manage.py runserver
```

Tüm endpointleri test etmek için tarayıcıdan şu adrese gidin:
```shell
http://localhost:8000/swagger/
```

## 3. Testler

Proje için CRUD işlemlerini, filtrelemeleri ve veri doğrulama senaryolarını kapsayan unit testler yazılmıştır.

Testleri **Docker** üzerinden çalıştırmak için:

```bash
docker-compose exec web python manage.py test api
```

Testleri **lokalde** çalıştırmak için:

```bash
python manage.py test api
```


### 4. API Endpoint Detayları

Aşağıdaki tablolar, API üzerindeki işlemleri ve kullanılabilir metodları özetlemektedir.

#### Dökümantasyon Arayüzü

| İşlem      | URL Yolu    | Metodlar                                                       | Açıklama                    |
| :--------- | :---------- | :------------------------------------------------------------- | :-------------------------- |
| Swagger UI | `/swagger/` | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square) | API dökümantasyonu arayüzü. |

#### 1. Kullanıcı İşlemleri (Users)

| İşlem                 | URL Yolu                  | Metodlar                                                          | Açıklama                                      |
| :-------------------- | :------------------------ | :---------------------------------------------------------------- | :-------------------------------------------- |
| Kullanıcı Listesi     | `/api/users/`             | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Kayıtlı tüm kullanıcıları listeler.           |
| Kullanıcı Oluştur     | `/api/users/`             | ![](https://img.shields.io/badge/POST-007ec6?style=flat-square)   | Yeni bir kullanıcı oluşturur.                 |
| Kullanıcı Detayı      | `/api/users/{id}/`        | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Belirtilen ID'ye sahip kullanıcıyı getirir.   |
| Kullanıcı Güncelle    | `/api/users/{id}/`        | ![](https://img.shields.io/badge/PUT-f9a825?style=flat-square)    | Kullanıcı bilgilerini tamamen değiştirir.     |
| Kullanıcı Düzenle     | `/api/users/{id}/`        | ![](https://img.shields.io/badge/PATCH-f9a825?style=flat-square)  | Kullanıcı bilgilerini kısmi olarak günceller. |
| Kullanıcı Sil         | `/api/users/{id}/`        | ![](https://img.shields.io/badge/DELETE-d32f2f?style=flat-square) | Kullanıcıyı sistemden siler.                  |
| Kullanıcı Gönderileri | `/api/users/{id}/posts/`  | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Kullanıcıya ait gönderileri listeler.         |
| Kullanıcı Albümleri   | `/api/users/{id}/albums/` | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Kullanıcıya ait albümleri listeler.           |
| Kullanıcı Görevleri   | `/api/users/{id}/todos/`  | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Kullanıcıya ait yapılacakları listeler.       |

#### 2. Gönderi İşlemleri (Posts)

| İşlem                 | URL Yolu                  | Metodlar                                                          | Açıklama                                           |
| :-------------------- | :------------------------ | :---------------------------------------------------------------- | :------------------------------------------------- |
| Post Listesi          | `/api/posts/`             | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Tüm gönderileri listeler.                          |
| Post Listesi (Filtre) | `/api/posts/?userId={id}` | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Belirli bir kullanıcıya ait gönderileri filtreler. |
| Post Oluştur          | `/api/posts/`             | ![](https://img.shields.io/badge/POST-007ec6?style=flat-square)   | Yeni bir gönderi oluşturur.                        |
| Post Detayı           | `/api/posts/{id}/`        | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Belirtilen ID'ye sahip gönderiyi getirir.          |
| Post Güncelle         | `/api/posts/{id}/`        | ![](https://img.shields.io/badge/PUT-f9a825?style=flat-square)    | Gönderi bilgilerini tamamen değiştirir.            |
| Post Düzenle          | `/api/posts/{id}/`        | ![](https://img.shields.io/badge/PATCH-f9a825?style=flat-square)  | Gönderi bilgilerini kısmi olarak günceller.        |
| Post Sil              | `/api/posts/{id}/`        | ![](https://img.shields.io/badge/DELETE-d32f2f?style=flat-square) | Gönderiyi siler.                                   |

#### 3. Yorum İşlemleri (Comments)

| İşlem                        | URL Yolu                       | Metodlar                                                          | Açıklama                                              |
| :--------------------------- | :----------------------------- | :---------------------------------------------------------------- | :---------------------------------------------------- |
| Yorum Listesi                | `/api/comments/`               | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Tüm yorumları listeler.                               |
| Yorum Listesi (Post Filtre)  | `/api/comments/?postId={id}`   | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Belirli bir gönderiye ait yorumları filtreler.        |
| Yorum Listesi (Email Filtre) | `/api/comments/?email={email}` | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Belirli bir e-posta adresine ait yorumları filtreler. |
| Yorum Oluştur                | `/api/comments/`               | ![](https://img.shields.io/badge/POST-007ec6?style=flat-square)   | Yeni bir yorum oluşturur.                             |
| Yorum Detayı                 | `/api/comments/{id}/`          | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Belirtilen ID'ye sahip yorumu getirir.                |
| Yorum Güncelle               | `/api/comments/{id}/`          | ![](https://img.shields.io/badge/PUT-f9a825?style=flat-square)    | Yorum bilgilerini tamamen değiştirir.                 |
| Yorum Düzenle                | `/api/comments/{id}/`          | ![](https://img.shields.io/badge/PATCH-f9a825?style=flat-square)  | Yorum bilgilerini kısmi olarak günceller.             |
| Yorum Sil                    | `/api/comments/{id}/`          | ![](https://img.shields.io/badge/DELETE-d32f2f?style=flat-square) | Yorumu siler.                                         |

#### 4. Albüm İşlemleri (Albums)

| İşlem                  | URL Yolu                 | Metodlar                                                          | Açıklama                                         |
| :--------------------- | :----------------------- | :---------------------------------------------------------------- | :----------------------------------------------- |
| Albüm Listesi          | `/api/albums/`           | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Tüm albümleri listeler.                          |
| Albüm Listesi (Filtre) | `/api/albums/?user={id}` | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Belirli bir kullanıcıya ait albümleri filtreler. |
| Albüm Oluştur          | `/api/albums/`           | ![](https://img.shields.io/badge/POST-007ec6?style=flat-square)   | Yeni bir albüm oluşturur.                        |
| Albüm Detayı           | `/api/albums/{id}/`      | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Belirtilen ID'ye sahip albümü getirir.           |
| Albüm Güncelle         | `/api/albums/{id}/`      | ![](https://img.shields.io/badge/PUT-f9a825?style=flat-square)    | Albüm bilgilerini tamamen değiştirir.            |
| Albüm Düzenle          | `/api/albums/{id}/`      | ![](https://img.shields.io/badge/PATCH-f9a825?style=flat-square)  | Albüm bilgilerini kısmi olarak günceller.        |
| Albüm Sil              | `/api/albums/{id}/`      | ![](https://img.shields.io/badge/DELETE-d32f2f?style=flat-square) | Albümü siler.                                    |

#### 5. Fotoğraf İşlemleri (Photos)

| İşlem                     | URL Yolu                  | Metodlar                                                          | Açıklama                                       |
| :------------------------ | :------------------------ | :---------------------------------------------------------------- | :--------------------------------------------- |
| Fotoğraf Listesi          | `/api/photos/`            | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Tüm fotoğrafları listeler.                     |
| Fotoğraf Listesi (Filtre) | `/api/photos/?album={id}` | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Belirli bir albüme ait fotoğrafları filtreler. |
| Fotoğraf Oluştur          | `/api/photos/`            | ![](https://img.shields.io/badge/POST-007ec6?style=flat-square)   | Yeni bir fotoğraf oluşturur.                   |
| Fotoğraf Detayı           | `/api/photos/{id}/`       | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Belirtilen ID'ye sahip fotoğrafı getirir.      |
| Fotoğraf Güncelle         | `/api/photos/{id}/`       | ![](https://img.shields.io/badge/PUT-f9a825?style=flat-square)    | Fotoğraf bilgilerini tamamen değiştirir.       |
| Fotoğraf Düzenle          | `/api/photos/{id}/`       | ![](https://img.shields.io/badge/PATCH-f9a825?style=flat-square)  | Fotoğraf bilgilerini kısmi olarak günceller.   |
| Fotoğraf Sil              | `/api/photos/{id}/`       | ![](https://img.shields.io/badge/DELETE-d32f2f?style=flat-square) | Fotoğrafı siler.                               |

#### 6. Görev İşlemleri (Todos)

| İşlem                           | URL Yolu                     | Metodlar                                                          | Açıklama                                         |
| :------------------------------ | :--------------------------- | :---------------------------------------------------------------- | :----------------------------------------------- |
| Todo Listesi                    | `/api/todos/`                | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Tüm görevleri listeler.                          |
| Todo Listesi (Kullanıcı Filtre) | `/api/todos/?user={id}`      | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Belirli bir kullanıcıya ait görevleri filtreler. |
| Todo Listesi (Durum Filtre)     | `/api/todos/?completed=true` | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Tamamlanma durumuna göre görevleri filtreler.    |
| Todo Oluştur                    | `/api/todos/`                | ![](https://img.shields.io/badge/POST-007ec6?style=flat-square)   | Yeni bir görev oluşturur.                        |
| Todo Detayı                     | `/api/todos/{id}/`           | ![](https://img.shields.io/badge/GET-2ea44f?style=flat-square)    | Belirtilen ID'ye sahip görevi getirir.           |
| Todo Güncelle                   | `/api/todos/{id}/`           | ![](https://img.shields.io/badge/PUT-f9a825?style=flat-square)    | Görev bilgilerini tamamen değiştirir.            |
| Todo Düzenle                    | `/api/todos/{id}/`           | ![](https://img.shields.io/badge/PATCH-f9a825?style=flat-square)  | Görev bilgilerini kısmi olarak günceller.        |
| Todo Sil                        | `/api/todos/{id}/`           | ![](https://img.shields.io/badge/DELETE-d32f2f?style=flat-square) | Görevi siler.                                    |
