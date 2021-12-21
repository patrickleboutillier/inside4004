const byte test0[] = {KCL, K2, KPLUS, K2, KPLUS, KEQ, KEND} ;
const byte test1[] = {KCL, KD, KD, KD, KR, KR, K1, K2, KDOT, K3, K4, KPLUS, K3, K4, KDOT, K5, K6, KMIN, K5, K6, KDOT, K7, K8, K9, KPLUS, KPLUS, KDOT, K1, K2, K3, KPLUS, KEQ, KEND} ;
const byte test2[] = {KCL, KD, KD, KR, K1, KDOT, K2, K3, KPLUS, K4, KDOT, K5, K6, KPLUS, KD, KD, KD, KD, KD, KD, KD, KEQ, KEND} ;
const byte test3[] = {KCL, KD, KD, KD, KR, KR, K1, K5, KDOT, K3, KPLUS, K5, K6, KDOT, K7, K8, K9, KMIN, K3, KDOT, K4, K5, K6, KPLUS, KEQ, KEND} ;
const byte test4[] = {KCL, KD, KD, KR, KR, K1, KHASH, K1, KPLUS, K2, KPLUS, K3, KPLUS, KHASH, K2, KHASH, K4, KPLUS, K5, KPLUS, K6, KPLUS, KHASH, K3, KHASH, K7, KPLUS, K8, KPLUS, K9, KPLUS, KHASH, KEQ, KEND} ;
const byte test5[] = {KCL, K1, K2, KDOT, K3, KMULT, K4, KDOT, K5, K6, KEQ, KEND} ;
const byte test6[] = {KCL, KD, KD, KR, K1, K2, KDOT, K3, KMULT, K4, KDOT, K5, K6, KEQ, KEND} ;
const byte test7[] = {KCL, KD, KD, KR, KR, K1, K2, KDOT, K3, KMULT, K4, KDOT, K5, K6, KEQ, KEND} ;
const byte test8[] = {KCL, K1, K2, KDOT, K3, KMULT, K4, KDOT, K5, K6, KMULT, KHASH, KDOT, K7, K8, K9, KEQ, KEND} ;
const byte test9[] = {KCL, K3, K6, K1, KDOT, K5, K2, KMULT, K1, K2, K0, KEQ, K1, K1, K8, KDOT, K6, KEQ, K9, K8, KDOT, K4, KEQ, KEND} ;
const byte test10[] = {KCL, K1, KDOT, K2, K5, KMULT, K1, K2, KEX, KEQ, K3, KDOT, K5, K0, KEQ, K1, KDOT, K9, K9, KEQ, KEND} ;
const byte test11[] = {KCL, K5, KMULT, KEQ, KEQ, KEQ, KEND} ;
const byte test12[] = {KCL, K1, K2, KDOT, K3, KDIV, KMULT, KDIV, KMULT, K4, KDOT, K5, K6, KEQ, KEND} ;
const byte test13[] = {KCL, K4, K0, KDIV, K6, KEQ, KEND} ;
const byte test14[] = {KCL, KD, KD, KR, K4, K0, KDIV, K6, KEQ, KEND} ;
const byte test15[] = {KCL, KD, KD, KR, KR, K4, K0, KDIV, K6, KEQ, KEND} ;
const byte test16[] = {KCL, K1, K2, K3, KDIV, K6, KDIV, KDOT, K7, K8, K9, KEQ, KEND} ;
const byte test17[] = {KCL, KD, KD, KR, K4, K5, K7, K8, KDIV, K3, K6, K0, KEQ, K2, K9, K0, K2, KEQ, K8, K7, K1, K6, KEQ, KEND} ;
const byte test18[] = {KCL, KD, KD, KR, K1, K2, K3, KDOT, K4, K5, KMP, KDIV, K3, K6, KDOT, K9, KEQ, KRM, KDIV, K2, K8, KDOT, K4, KEQ, KRM, KDIV, K3, K1, KDOT, K5, K5, KEQ, KEND} ;
const byte test19[] = {KCL, K1, K2, K3, K4, K5, KMULT, K2, KPCT, KEND} ;

const byte test20[] = {KCL, K2, KDIV, K3, KPCT, KEND} ;
const byte test21[] = {KCL, KD, KD, KR, KCL, K1, KDOT, K5, KPLUS, K1, K2, K9, KDOT, K0, K5, KPLUS, K1, K1, KDOT, K0, K8, KMIN, KMULT, K1, K2, KDOT, K4, KDIV, KDOT, K5, K5, KDIV, K1, K2, KDOT, K9, K6, KPLUS, K3, KDOT, K5, K6, KMIN, KEQ, KDIV, K0, KDOT, K8, K7, KEQ, KEND} ;
const byte test22[] = {KCL, KD, KD, KR, KCL, K1, K2, K3, KDIV, K1, K2, K3, KPLUS, K4, K5, K6, KPLUS, K7, K8, K9, KPLUS, KEQ, KPCT, KPLUS, K4, K5, K6, KPCT, KPLUS, K7, K8, K9, KPCT, KPLUS, KEQ, KEND} ;
const byte test23[] = {KCL, KD, KD, KR, KR, K1, KDOT, K2, K3, KMULT, K4, KEQ, KPLUS, K5, KDOT, K6, K7, KMULT, K8, KEQ, KPLUS, KDIV, K3, KEX, KEQ, KEND} ;
const byte test24[] = {KCL, KD, KD, KR, KCM, K1, K2, K3, KDOT, K4, K5, KMULT, K2, K3, KDOT, K4, KMEP, K4, K2, KDOT, K6, KMEM, K5, K1, KMEP, KCM, KEND} ;
const byte test25[] = {KCL, KD, KD, KR, KCM, K4, K5, K7, K8, KDIV, K3, K6, K0, KMEP, K2, K9, K0, K2, KMEP, K8, K7, K1, K6, KMEM, KCM, KEND} ;
const byte test26[] = {KCL, KR, KCM, KCL, K1, K2, K3, K4, K5, K6, K7, K8, K9, KDIV, K1, K2, K3, KPLUS, K4, K5, K6, KPLUS, K7, K8, K9, KPLUS, KEQ, KMULT, K1, K2, K3, KMEP, K4, K5, K6, KMEP, K7, K8, K9, KMEP, KCM, KEND} ;
const byte test27[] = {KCL, KD, KD, KR, K1, K1, KMULT, K1, KDOT, K2, K3, KMEP, K1, K2, KMULT, K4, KDOT, K1, K1, KMEP, K3, KMULT, K2, KDOT, K0, K3, KMEP, KRM, KMULT, K1, K0, KPCT, KMM, KRM, KMULT, K5, KPCT, KMP, K2, KDOT, K5, K0, KMP, KCM, KEND} ;
const byte test28[] = {KCL, KD, KD, KR, KR, KCM, KCL, K1, K0, KMP, KMULT, K2, KDOT, K3, K8, KEQ, KPLUS, K2, K0, KMP, KMULT, K1, KDOT, K3, K8, KEQ, KPLUS, K1, K5, KMP, KMULT, K3, KDOT, K6, K5, KEQ, KPLUS, KDIV, KCM, KEQ, KEND} ;
const byte test29[] = {KCL, KD, KD, K1, K5, K2, K4, K1, K7, K5, K4, K3, KDOT, K0, K6, K2, K5, KSQ, KEND} ;
const byte test30[] = {KCL, KD, KD, KD, KD, KD, KD, KR, K2, KMP, KMULT, KEQ, KPLUS, K3, KMP, KMULT, KEQ, KPLUS, K4, KMP, KMULT, KEQ, KPLUS, K5, KMP, KMULT, KEQ, KPLUS, K6, KMP, KMULT, KEQ, KPLUS, KMULT, K5, KEQ, KPLUS, KCM, KMULT, KEQ, KMIN, KDIV, K5, KEQ, KEQ, KSQ, KEND} ;
const byte test31[] = {KCL, KD, KD, KD, KD, KD, KD, KR, KCL, KCM, K1, K2, KMULT, KMEP, K8, KMULT, KMEP, KCM, KSQ, KEND} ;
const byte test32[] = {KCL, KD, KD, KD, KD, KD, KD, KR, KR, K1, K2, K3, K4, K5, K6, K7, K8, KPLUS, KEQ, KEND} ;
const byte test33[] = {KCL, KD, KD, KD, KD, KD, KD, KR, KR, K1, K2, K3, K4, K5, K6, K7, K8, K9, KPLUS, KEQ, KEND} ;
const byte test34[] = {KCL, KD, KD, KD, KD, KD, KD, KD, KD, KR, KR, K9, K0, K0, K0, K0, K0, KPLUS, K1, K0, K0, K0, K0, K0, KPLUS, KCE, KPLUS, KEQ, KEND} ;
const byte test35[] = {KCL, K1, K2, K3, K4, K5, K6, K7, K8, K9, KMULT, K1, K0, K0, K0, K0, K0, KEQ, KEND} ;
const byte test36[] = {KCL, K1, K2, K3, K4, K5, K6, K7, K8, K9, KMULT, K1, K0, K0, K0, K0, K0, K0, KEQ, KEND} ;
const byte test37[] = {KCL, KD, KD, KD, KD, KD, KD, KD, KD, KR, K1, K2, K3, K4, K5, K6, KMULT, K1, KEQ, KEND} ;
const byte test38[] = {KCL, KD, KD, KD, KD, KD, KD, KD, KD, KR, K1, K2, K3, K4, K5, K6, K7, KMULT, K1, KEQ, KEND} ;
const byte test39[] = {KCL, K4, K0, K0, K0, K0, K0, K0, KDIV, K0, KDOT, K0, K0, K0, K0, K0, K0, K3, KEQ, KEND} ;
const byte test40[] = {KCL, K4, K0, K0, K0, K0, K0, K0, K0, KDIV, K0, KDOT, K0, K0, K0, K0, K0, K0, K3, KEQ, KEND} ;
const byte test41[] = {KCL, KD, KD, KD, KD, KD, KD, KD, KD, KR, KR, K4, K0, K0, K0, K0, K0, KDIV, K3, KEQ, KEND} ;
const byte test42[] = {KCL, KD, KD, KD, KD, KD, KD, KD, KD, KR, KR, K4, K0, K0, K0, K0, K0, K0, KDIV, K3, KEQ, KEND} ;

const byte *tests[] = {
  test0,
  test1,
  test2,
  test3,
  test4,
  test5,
  test6,
  test7,
  test8,
  test9,
  test10,
  test11,
  test12,
  test13,
  test14,
  test15,
  test16,
  test17,
  test18,
  test19,
  test20,
  test21,
  test22,
  test23,
  test24,
  test25,
  test26,
  test27,
  test28,
  test29,
  test30,
  test31,
  test32,
  test33,
  test34,
  test35,
  test36,
  test37,
  test38,
  test39,
  test40,
  test41,
  test42, 
  NULL
} ;
