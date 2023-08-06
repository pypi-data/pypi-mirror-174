# Ruqia lib
This library used for Arabic NLP to process, prepare and clean the Arabic text   


مكتبة مخصصة لخدمة معالجة اللغة العربية وتشمل عدد من الوظائف لتنظيف النصوص وغيرها

## Install
```
pip install ruqia
```
## Use
```
from ruqiya import ruqiya
```
## Example
```
text="""
!!أهلا وسهلا بك 👋 في الإصدار الأول من مكتبة رقيا
هل هي المرة الأولى التي تستخدم فيها المكتبة😀؟!!
للتواصل ايميل
example@email.com
الموقع
https://pypi.org/project/ruqia/
تويتر
@Ru0Sa
#Arabic_NLP

"""
```
## Clean the text. It includes all functions
```
text_cleaned1=ruqiya.clean_text(text)
print(text_cleaned1)
```
## Remove repeating character
```
text_cleaned2=ruqiya.remove_repeating_char(text)
print(text_cleaned2)

```
## Remove punctuations
```
text_cleaned3=ruqiya.remove_punctuations(text)
print(text_cleaned3)
```
## Normalize Arabic

```
text_cleaned4=ruqiya.normalize_arabic(text)
print(text_cleaned4)
```
## Remove diacritics

```
text_cleaned5=ruqiya.remove_diacritics(text)
print(text_cleaned5)
```
## Remove stop words

```
text_cleaned6=ruqiya. remove_stop_words(text)
print(text_cleaned6)

```
## Remove emojis

```
text_cleaned7=ruqiya. remove_emojis(text)
print(text_cleaned7)

```

## Remove mentions

```
text_cleaned8=ruqiya. remove_mentions(text)
print(text_cleaned8)

```

## Remove hashtags

```
text_cleaned9=ruqiya. remove_hashtags(text)
print(text_cleaned9)

```
## Remove emails

```
text_cleaned10=ruqiya. remove_emails(text)
print(text_cleaned10)

```
## Remove URLs

```
text_cleaned11=ruqiya. remove_URLs(text)
print(text_cleaned11)

```