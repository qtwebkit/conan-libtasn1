#include <iostream>
#include <libtasn1.h>

int main()
{
    std::cout << "tasn1 version: " << asn1_check_version(ASN1_VERSION) << std::endl;
    return 0;
}

