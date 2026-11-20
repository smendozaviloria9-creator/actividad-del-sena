cantidad_botellas = 2
precio_botella = 2500


cantidad_frutas = 1
precio_frutas =1800


minimo_para_descuento = 10000
valor_descuento= 1000


cont_botellas = cantidad_botellas * precio_botella
cont_frutas = cantidad_frutas * precio_frutas
subtotal = cont_botellas + cont_frutas


if subtotal >=minimo_para_descuento:
    total_a_pagar = subtotal - valor_descuento
    aplico_descuento = True
else:
    total_a_pagar = subtotal
    aplico_descuento = False


print(f"subtotal: ${subtotal}")
print(f"aplicar descuento?: {'si' if aplico_descuento else 'no'}")
print(f"total a pagar: ${total_a_pagar}")