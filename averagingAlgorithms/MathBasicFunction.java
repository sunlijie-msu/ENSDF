/*     */ package averagingAlgorithms;
/*     */ 
/*     */ import java.util.function.DoubleFunction;
/*     */ import java.util.stream.DoubleStream;
/*     */ 
/*     */ public class MathBasicFunction {
/*     */   public static final double[] product(double[] x, double[] y) {
/*  25 */     double[] z = new double[x.length];
/*  26 */     for (int i = 0; i < x.length; i++)
/*  27 */       z[i] = x[i] * y[i]; 
/*  29 */     return z;
/*     */   }
/*     */   
/*     */   public static final double sum(double[] x) {
/*  47 */     return DoubleStream.of(x).sum();
/*     */   }
/*     */   
/*     */   public static final double weightedSum(double[] x, double[] weights) {
/*  62 */     double weightSum = sum(weights);
/*  63 */     double result = 0.0D;
/*  64 */     int n = x.length;
/*  65 */     for (int i = 0; i < n; i++)
/*  66 */       result += x[i] * weights[i] / weightSum; 
/*  69 */     return result;
/*     */   }
/*     */   
/*     */   public static final double max(double[] x) {
/*  78 */     return (new arrayMaxMin(x)).max;
/*     */   }
/*     */   
/*     */   public static final double min(double[] x) {
/*  87 */     return (new arrayMaxMin(x)).min;
/*     */   }
/*     */   
/*     */   public static final int maxInd(double[] x) {
/*  96 */     return (new arrayMaxMin(x)).maxInd;
/*     */   }
/*     */   
/*     */   public static final int minInd(double[] x) {
/* 105 */     return (new arrayMaxMin(x)).minInd;
/*     */   }
/*     */   
/*     */   public static final double abs(double x) {
/* 114 */     return Math.abs(x);
/*     */   }
/*     */   
/*     */   public static final double[] abs(double[] x) {
/* 127 */     double[] result = new double[x.length];
/* 128 */     for (int i = 0; i < x.length; i++)
/* 129 */       result[i] = Math.abs(x[i]); 
/* 131 */     return result;
/*     */   }
/*     */   
/*     */   public static final double findMax(DoubleFunction<Double> f, double lowerBound, double upperBound) {
/* 145 */     int N = 100;
/* 146 */     double eps = 1.0E-20D;
/* 152 */     double[] x = new double[100];
/* 153 */     double[] fx = new double[100];
/* 154 */     double b = upperBound;
/* 155 */     double a = lowerBound;
/* 156 */     while (b - a > 1.0E-20D) {
/* 157 */       double d = (b - a) / 99.0D;
/*     */       int j;
/* 158 */       for (j = 0; j < 100; j++) {
/* 159 */         x[j] = a + d * j;
/* 160 */         fx[j] = ((Double)f.apply(x[j])).doubleValue();
/*     */       } 
/* 162 */       j = maxInd(fx);
/*     */       try {
/* 164 */         a = x[j - 1];
/* 165 */         b = x[j + 1];
/* 166 */       } catch (ArrayIndexOutOfBoundsException e) {
/* 167 */         if (j == 0) {
/* 168 */           b = x[1];
/*     */           continue;
/*     */         } 
/* 170 */         a = x[j - 1];
/*     */       } 
/*     */     } 
/* 174 */     double dx = (b - a) / 99.0D;
/*     */     int i;
/* 175 */     for (i = 0; i < 100; i++) {
/* 176 */       x[i] = a + dx * i;
/* 177 */       fx[i] = ((Double)f.apply(x[i])).doubleValue();
/*     */     } 
/* 179 */     i = maxInd(fx);
/* 180 */     return x[i];
/*     */   }
/*     */   
/*     */   public static final double uniroot(DoubleFunction<Double> f, double lowerBound, double upperBound) throws IllegalArgumentException {
/* 196 */     double a, b, eps = 1.0E-20D;
/* 197 */     int maxit = 5000;
/* 202 */     double fa = ((Double)f.apply(lowerBound)).doubleValue();
/* 203 */     double fb = ((Double)f.apply(upperBound)).doubleValue();
/* 206 */     if (fa * fb > 0.0D)
/* 207 */       throw new IllegalArgumentException("uniroot: The given function does not have a root within the specified interval"); 
/* 210 */     if (Math.abs(fa) < Math.abs(fb)) {
/* 211 */       a = upperBound;
/* 212 */       b = lowerBound;
/*     */     } else {
/* 214 */       a = lowerBound;
/* 215 */       b = upperBound;
/*     */     } 
/* 218 */     double c = a;
/* 219 */     double d = 0.0D;
/* 220 */     boolean mflag = true;
/* 221 */     int count = 0;
/* 222 */     while (Math.abs(a - b) > 1.0E-20D && Math.abs(fb) > 1.0E-20D && count < 5000) {
/*     */       double s;
/* 223 */       fa = ((Double)f.apply(a)).doubleValue();
/* 224 */       fb = ((Double)f.apply(b)).doubleValue();
/* 225 */       double fc = ((Double)f.apply(c)).doubleValue();
/* 227 */       if (fa != fc && fb != fc) {
/* 229 */         s = a * fb * fc / (fa - fb) * (fa - fc) + b * fa * fc / (fb - fa) * (fb - fc) + 
/* 230 */           c * fa * fb / (fc - fa) * (fc - fb);
/*     */       } else {
/* 233 */         s = b - fb * (b - a) / (fb - fa);
/*     */       } 
/* 236 */       boolean useBisection = false;
/* 237 */       useBisection = !(!useBisection && 0.75D * a + 0.25D * b >= s && s <= b);
/* 238 */       useBisection = !(!useBisection && (!mflag || Math.abs(s - b) < 0.5D * Math.abs(b - c)));
/* 239 */       useBisection = !(!useBisection && (mflag || Math.abs(s - b) < 0.5D * Math.abs(c - d)));
/* 240 */       useBisection = !(!useBisection && (!mflag || Math.abs(b - c) >= 1.0E-20D));
/* 241 */       useBisection = !(!useBisection && (mflag || Math.abs(b - c) >= 1.0E-20D));
/* 243 */       if (useBisection) {
/* 244 */         s = 0.5D * (a + b);
/* 245 */         mflag = true;
/*     */       } else {
/* 247 */         mflag = false;
/*     */       } 
/* 250 */       d = c;
/* 251 */       c = b;
/* 252 */       double fs = ((Double)f.apply(s)).doubleValue();
/* 254 */       if (fa * fs < 0.0D) {
/* 255 */         b = s;
/* 256 */         fb = fs;
/*     */       } else {
/* 258 */         a = s;
/* 259 */         fa = fs;
/*     */       } 
/* 262 */       if (Math.abs(fa) < Math.abs(fb)) {
/* 264 */         double tmp = a;
/* 265 */         a = b;
/* 266 */         b = tmp;
/* 269 */         tmp = fa;
/* 270 */         fa = fb;
/* 271 */         fb = tmp;
/*     */       } 
/* 273 */       count++;
/*     */     } 
/* 276 */     return b;
/*     */   }
/*     */ }


/* Location:              D:\X\ND\ENSDF\AverageTool_22January2025.jar!\averagingAlgorithms\MathBasicFunction.class
 * Java compiler version: 8 (52.0)
 * JD-Core Version:       1.1.3
 */