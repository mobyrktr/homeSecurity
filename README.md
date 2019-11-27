# Yeni Kullanıcı Ekleme

**_Daha sonra, bu aşamaların hiçbirine gerek kalmadan bir fonksiyon aracığıyla kullanıcı kaydı yapılacaktır._**

* Dataset Oluşturma*
* Eğitim*
* ID - İsim Eşleştirmesi
* Ses Dosyalarını Oluşturma

*: Zorunlu
### 1) Dataset Oluşturma 
**dataSetCreator.py** adlı dosyayı çalıştırdığınızda kullanıcıya vermek istediğiniz ID sorulacaktır. 
ID'yi yazdıktan sonra varsayılan kameranız tarafından 21 adet görüntü alınacaktır.
Kodun doğru çalışabilmesi için görüntüler alınırken hareket etmemeye özen göstermelisiniz.

### 2) Eğitim
Bu aşamada sadece **trainer.py** adlı dosyayı çalıştırmanız yeterli olacaktır.

### 3) ID - İsim Eşleştirmesi
Eğitim aşamasını geçtikten sonra **faceDetector.py** adlı dosyadaki labels adlı sözlükte aşağıdaki şekilde bir değişiklik yapılmalıdır. 
```python
labels = {1:"<isim1>", 2: "<isim2>"}
```
Bu sayede ilk aşamada kullanıcı için vermiş olduğunuz ID'yi kullanıcının ismiyle eşleştirmiş olacaksınız.

### 4) Ses Dosyalarını Oluşturma
Eve giriş yaptığınızda isminizin *Hoşgeldin -isminiz-* şeklinde okunmasını istiyorsanız bu aşamayı da tamamlamalısınız. 
Tek yapmanız gereken **TTS.py** adlı dosyanın sonuna
```python
girisKayit("isminiz")
```
şeklinde bir satır eklemek.
