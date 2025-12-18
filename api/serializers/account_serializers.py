from rest_framework import serializers
from api.models.accounts import Address, Company, Geo, User

class CompanySerializer(serializers.ModelSerializer):
    """User serializer icinde nested olarak kullanilan sirket bilgisi."""
    class Meta:
        model = Company
        fields = ['name']
        
class GeoSerializer(serializers.ModelSerializer):
    """Address serializer icindeki cografi koordinatlari (lat/lng) temsil eder."""
    class Meta:
        model = Geo
        fields = ['lat', 'lng']

class AddressSerializer(serializers.ModelSerializer):
    """
    Adres bilgilerini ve bagli oldugu Geo (koordinat) verisini yonetir.  
    UserSerializer tarafindan nested yapı olarak cagirilir.
    """
    geo = GeoSerializer()

    class Meta:
        model = Address
        fields = ['street', 'suite', 'city', 'zipcode', 'geo']


class UserSerializer(serializers.ModelSerializer):
    """
    Kullanici profilinin tamamini (Address, Geo, Company dahil) yonetir.  

    Standart CRUD islemlerinin haricinde, create ve update metodlari   
    override edilerek nested verilerin yazilmasi ve guncellenmesi saglanir.
    """
    address = AddressSerializer()
    company = CompanySerializer()

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'website', 'phone', 'address', 'company']

    def create(self, validated_data):
        """
        Nested veri yapisiyla yeni kullanici olusturur.
        Bu metot varsayilan create islemini override eder.
        Tek bir JSON payload icindeki 'address', 'geo' ve 'company' verilerini
        ayristirir ve sirayla kaydeder.

        Args:
            validated_data (dict): Serializer tarafindan dogrulanmis ham veri.
        
        Returns:
            User: Olusturulan kullanici objesi.
        """
        address_data = validated_data.pop('address')
        company_data = validated_data.pop('company')
        geo_data = address_data.pop('geo')

        user = User.objects.create(**validated_data)
        Company.objects.create(user=user, **company_data)
        address = Address.objects.create(user=user, **address_data)
        Geo.objects.create(address=address, **geo_data)

        return user
    
    def update(self, instance, validated_data):
        """
        Nested veri yapisiyla kullaniciyi ve iliskili verileri gunceller.

        Bu metot varsayilan update islemini override eder.
        Payload icerisindeki 'address', 'geo' ve 'company' verilerini ayristirip
        ilgili iliskisel kayitlari gunceller.

        Args:
            instance (User): Guncellenecek mevcut kullanici objesi.
            validated_data (dict): Serializer tarafindan dogrulanmis yeni veriler.

        Returns:
            User: Guncellenmis kullanici objesi.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.website = validated_data.get('website', instance.website)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()

        if 'company' in validated_data:
            company_data = validated_data.pop('company')
            company = instance.company
            company.name = company_data.get('name', company.name)
            company.save()
        
        if 'address' in validated_data:
            address_data = validated_data.pop('address')
            geo_data = address_data.pop('geo', None)
            address = instance.address
            address.street = address_data.get('street', address.street)
            address.city = address_data.get('city', address.city)
            address.suite = address_data.get('suite', address.suite)
            address.zipcode = address_data.get('zipcode', address.zipcode)
            address.save()

            if geo_data:
                geo = address.geo
                geo.lat = geo_data.get('lat', geo.lat)
                geo.lng = geo_data.get('lng', geo.lng)
                geo.save()
        
        return instance