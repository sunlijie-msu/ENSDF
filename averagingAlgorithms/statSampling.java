/*     */ package averagingAlgorithms;
/*     */ 
/*     */ import java.util.Random;
/*     */ 
/*     */ public class statSampling {
/*     */   public static final double[] runif(int n) {
/*  31 */     double[] result = new double[n];
/*  32 */     for (int i = 0; i < n; i++)
/*  33 */       result[i] = Math.random(); 
/*  35 */     return result;
/*     */   }
/*     */   
/*     */   public static final double[] rnorm(int n, double mean, double sd) {
/*  52 */     Random generator = new Random();
/*  53 */     double[] result = new double[n];
/*  54 */     for (int i = 0; i < n; i++)
/*  55 */       result[i] = generator.nextGaussian() * sd + mean; 
/*  57 */     return result;
/*     */   }
/*     */   
/*     */   public static final double rnorm(double mean, double sd) {
/*  66 */     return rnorm(1, mean, sd)[0];
/*     */   }
/*     */   
/*     */   public static final double[] rAnorm(int n, double peak, double lowSD, double upSD) {
/*  83 */     double[] u = runif(n);
/*  84 */     double[] result = new double[n];
/*  85 */     for (int i = 0; i < n; i++) {
/*  86 */       if (u[i] < lowSD / (upSD + lowSD)) {
/*  87 */         result[i] = peak - Math.abs(rnorm(0.0D, lowSD));
/*     */       } else {
/*  89 */         result[i] = peak + Math.abs(rnorm(0.0D, upSD));
/*     */       } 
/*     */     } 
/*  92 */     return result;
/*     */   }
/*     */   
/*     */   public static final double rAnorm(double peak, double lowSD, double upSD) {
/* 103 */     return rAnorm(1, peak, lowSD, upSD)[0];
/*     */   }
/*     */   
/*     */   public static final int[] rInt(int n, int low, int high) {
/* 120 */     Random generator = new Random();
/* 121 */     int[] result = new int[n];
/* 122 */     for (int i = 0; i < n; i++)
/* 123 */       result[i] = generator.nextInt(high - low) + low; 
/* 125 */     return result;
/*     */   }
/*     */   
/*     */   public static final int rInt(int low, int high) {
/* 136 */     return rInt(1, low, high)[0];
/*     */   }
/*     */   
/*     */   public static final int[] sample(int low, int high, int size) {
/* 155 */     int n = high - low;
/* 156 */     int[] numbers = new int[n];
/*     */     int i;
/* 157 */     for (i = 0; i < n; i++)
/* 158 */       numbers[i] = low + i; 
/* 160 */     int max = n;
/* 161 */     int[] result = new int[size];
/* 162 */     for (int count = 0; count < size; count++) {
/* 163 */       i = rInt(0, max);
/* 164 */       result[count] = numbers[i];
/* 165 */       numbers[i] = numbers[max - 1];
/* 166 */       max--;
/*     */     } 
/* 169 */     return result;
/*     */   }
/*     */ }


/* Location:              D:\X\ND\ENSDF\AverageTool_22January2025.jar!\averagingAlgorithms\statSampling.class
 * Java compiler version: 8 (52.0)
 * JD-Core Version:       1.1.3
 */