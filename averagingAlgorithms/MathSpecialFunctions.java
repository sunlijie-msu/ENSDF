/*     */ package averagingAlgorithms;
/*     */ 
/*     */ import ensdf_datapoint.dataPt;
/*     */ import org.apache.commons.math3.special.Erf;
/*     */ import org.apache.commons.math3.special.Gamma;
/*     */ import org.apache.commons.math3.util.CombinatoricsUtils;
/*     */ 
/*     */ public class MathSpecialFunctions {
/*     */   public static final double factorial(int n) {
/*  29 */     return CombinatoricsUtils.factorialDouble(n);
/*     */   }
/*     */   
/*     */   public static final double erf(double x) {
/*  39 */     return Erf.erf(x);
/*     */   }
/*     */   
/*     */   public static final double erfc(double x) {
/*  50 */     return Erf.erfc(x);
/*     */   }
/*     */   
/*     */   public static final double normalIntegral(dataPt d, double x) {
/*  66 */     double v = d.getValue();
/*  67 */     double l = d.getLower();
/*  68 */     double u = d.getUpper();
/*  69 */     if (x <= d.getValue())
/*  70 */       return l / (l + u) * (1.0D + erf((x - v) / Math.sqrt(2.0D) * l)); 
/*  72 */     return u / (u + l) * erf((x - v) / Math.sqrt(2.0D) * u) + l / (u + l);
/*     */   }
/*     */   
/*     */   public static double GaussianArea(dataPt d, double a, double b) {
/*  90 */     return normalIntegral(d, b) - normalIntegral(d, a);
/*     */   }
/*     */   
/*     */   public static final double inverseErf(double y0) {
/* 100 */     return Erf.erfInv(y0);
/*     */   }
/*     */   
/*     */   public static final double GammaFunction(double x) {
/* 110 */     return Gamma.gamma(x);
/*     */   }
/*     */   
/*     */   public static final double lngamma(double x) {
/* 120 */     return Gamma.logGamma(x);
/*     */   }
/*     */   
/*     */   public static final double regularizedLowerIncompleteGamma(double a, double x) {
/* 133 */     return Gamma.regularizedGammaP(a, x);
/*     */   }
/*     */   
/*     */   public static final double regularizedUpperIncompleteGamma(double a, double x) {
/* 146 */     return Gamma.regularizedGammaQ(a, x);
/*     */   }
/*     */   
/*     */   public static final double lowerIncompleteGamma(double a, double x) {
/* 159 */     return GammaFunction(a) * regularizedLowerIncompleteGamma(a, x);
/*     */   }
/*     */   
/*     */   public static final double upperIncompleteGamma(double a, double x) {
/* 172 */     return GammaFunction(a) * regularizedUpperIncompleteGamma(a, x);
/*     */   }
/*     */   
/*     */   public static final double invLowerIncompleteGamma(double s, double y) {
/* 192 */     double precision = 1.0E-6D;
/* 194 */     int maxIterations = 2000;
/* 205 */     double lower = 0.0D;
/* 206 */     double upper = 10.0D;
/* 207 */     double gLower = y;
/* 208 */     double gUpper = y - lowerIncompleteGamma(s, upper);
/* 209 */     double middle = (upper + lower) / 2.0D;
/* 210 */     double gMiddle = y - lowerIncompleteGamma(s, middle);
/* 213 */     while (gUpper >= 0.0D) {
/* 214 */       lower = upper;
/* 215 */       gLower = gUpper;
/* 216 */       upper *= 1.1D;
/* 217 */       gUpper = y - lowerIncompleteGamma(s, upper);
/*     */     } 
/* 220 */     boolean bisectionFail = false;
/* 221 */     for (int i = 1; i <= maxIterations; i++) {
/* 222 */       middle = (upper + lower) / 2.0D;
/* 223 */       gMiddle = y - lowerIncompleteGamma(s, middle);
/* 225 */       if (Math.abs(gMiddle) < precision)
/*     */         break; 
/* 227 */       if (gMiddle < 0.0D) {
/* 228 */         upper = middle;
/*     */       } else {
/* 230 */         lower = middle;
/*     */       } 
/* 233 */       if (i == maxIterations)
/* 234 */         bisectionFail = true; 
/*     */     } 
/* 239 */     if (bisectionFail) {
/* 240 */       double diffSign = Math.signum(gMiddle);
/* 241 */       double dMiddle = 0.1D;
/* 242 */       while (Math.abs(gMiddle) > precision && dMiddle > precision) {
/* 243 */         middle += diffSign * dMiddle;
/* 244 */         gMiddle = y - lowerIncompleteGamma(s, middle);
/* 245 */         if (Math.signum(gMiddle) != diffSign) {
/* 246 */           middle -= diffSign * dMiddle;
/* 247 */           dMiddle *= 0.1D;
/*     */         } 
/*     */       } 
/*     */     } 
/* 251 */     return middle;
/*     */   }
/*     */ }


/* Location:              D:\X\ND\ENSDF\AverageTool_22January2025.jar!\averagingAlgorithms\MathSpecialFunctions.class
 * Java compiler version: 8 (52.0)
 * JD-Core Version:       1.1.3
 */