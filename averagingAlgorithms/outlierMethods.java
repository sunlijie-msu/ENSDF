/*     */ package averagingAlgorithms;
/*     */ 
/*     */ import ensdf_datapoint.dataPt;
/*     */ import java.util.ArrayList;
/*     */ import java.util.Arrays;
/*     */ import java.util.Collections;
/*     */ import java.util.List;
/*     */ 
/*     */ public class outlierMethods {
/*     */   public static final dataPt[] ChauvenetCriterion(dataPt[] dataset) {
/*  31 */     int i = 0;
/*  32 */     int n = 0;
/*  40 */     n = dataset.length;
/*  41 */     boolean leaveLoop = false;
/*  42 */     List<dataPt> outliers = new ArrayList<>();
/*  43 */     List<dataPt> points = new ArrayList<>();
/*  44 */     dataPt[] dataPt_arr = new dataPt[0];
/*  46 */     for (i = 0; i < n; i++)
/*  47 */       points.add(dataset[i]); 
/*  50 */     while (!leaveLoop) {
/*  51 */       n = points.size();
/*  52 */       leaveLoop = true;
/*  53 */       dataPt unwtAv = averagingMethods.unweightedAverage(points.<dataPt>toArray(dataPt_arr));
/*  54 */       double mean = unwtAv.getValue();
/*  57 */       double stdDev = unwtAv.getLower() * Math.sqrt(n);
/*  58 */       double maxDev = Math.sqrt(2.0D) * MathSpecialFunctions.inverseErf(((
/*  59 */           2 * n) - 1.0D) / (2 * n)) * stdDev;
/*  61 */       int rejectNum = 0;
/*  62 */       for (i = 0; i < n; i++) {
/*  63 */         if (Math.abs(((dataPt)points.get(i - rejectNum)).getValue() - mean) > 
/*  64 */           maxDev) {
/*  65 */           outliers.add(points.get(i - rejectNum));
/*  66 */           points.remove(i - rejectNum);
/*  67 */           leaveLoop = false;
/*  68 */           rejectNum++;
/*     */         } 
/*     */       } 
/*     */     } 
/*  72 */     return outliers.<dataPt>toArray(dataPt_arr);
/*     */   }
/*     */   
/*     */   public static final dataPt[] BirchCriterion(dataPt[] dataset, dataPt givenMean, double k) {
/* 106 */     int n = dataset.length;
/* 107 */     double mean = givenMean.getValue();
/* 108 */     double meanVariance = givenMean.gaussVariance();
/* 110 */     List<dataPt> sortedSet = new ArrayList<>();
/*     */     int i;
/* 112 */     for (i = 0; i < n; i++)
/* 113 */       sortedSet.add(dataset[i]); 
/* 117 */     Collections.sort(sortedSet, 
/* 118 */         dataPt.normalizedDeviationComparatorConstructor(mean));
/* 120 */     List<dataPt> outliers = new ArrayList<>();
/* 121 */     dataPt[] dataPt_arr = new dataPt[0];
/* 123 */     int rejectNum = 0;
/* 124 */     for (i = 0; i < n; i++) {
/* 125 */       double deviation = Math.abs(((dataPt)sortedSet.get(i)).getValue() - mean);
/* 126 */       double totalVariance = ((dataPt)sortedSet.get(i)).gaussVariance() + 
/* 127 */         meanVariance;
/* 128 */       if (0.5D + 0.5D * MathSpecialFunctions.erf(deviation / 
/* 129 */           Math.sqrt(2.0D * totalVariance)) > k) {
/* 130 */         outliers.add(sortedSet.get(i));
/* 131 */         rejectNum++;
/*     */       } 
/* 133 */       if (n - rejectNum < 3)
/*     */         break; 
/*     */     } 
/* 137 */     return outliers.<dataPt>toArray(dataPt_arr);
/*     */   }
/*     */   
/*     */   public static final dataPt[] BirchCriterion(dataPt[] dataset, double k) {
/* 150 */     return BirchCriterion(dataset, averagingMethods.weightedAverage(dataset), k);
/*     */   }
/*     */   
/*     */   public static final dataPt[] BirchCriterion(dataPt[] dataset, dataPt givenMean) {
/* 161 */     return BirchCriterion(dataset, givenMean, 0.99D);
/*     */   }
/*     */   
/*     */   public static final dataPt[] BirchCriterion(dataPt[] dataset) {
/* 172 */     return BirchCriterion(dataset, averagingMethods.weightedAverage(dataset), 0.99D);
/*     */   }
/*     */   
/*     */   public static final double calcPeircesMaxNormDev(int numPts, int numOutliers) {
/* 187 */     double precision = 1.0E-12D;
/* 188 */     double sqrt2 = Math.sqrt(2.0D);
/* 192 */     double NlnQ = 0.0D;
/* 193 */     double lambda = 0.0D;
/* 194 */     double x = 0.0D;
/* 195 */     double R = 1.0D;
/* 196 */     double newR = 0.0D;
/* 197 */     double result = 0.0D;
/* 199 */     NlnQ = numOutliers * Math.log(numOutliers) + (
/* 200 */       numPts - numOutliers) * Math.log((numPts - numOutliers)) - 
/* 201 */       numPts * Math.log(numPts);
/*     */     while (true) {
/* 206 */       lambda = Math.exp((NlnQ - numOutliers * Math.log(R)) / (
/* 207 */           numPts - numOutliers));
/* 209 */       x = Math.sqrt(1.0D + (numPts - numOutliers - 1) * (
/* 210 */           1.0D - lambda * lambda) / numOutliers);
/* 212 */       newR = Math.exp(0.5D * (x * x - 1.0D)) * 
/* 213 */         MathSpecialFunctions.erfc(x / sqrt2);
/* 214 */       if (Math.abs(R - newR) < 1.0E-12D)
/*     */         break; 
/* 217 */       R = newR;
/*     */     } 
/* 221 */     result = x;
/* 222 */     return result;
/*     */   }
/*     */   
/*     */   public static final dataPt[] PeirceCriterion(dataPt[] dataset) {
/* 241 */     int n = dataset.length;
/* 243 */     dataPt unwtAv = averagingMethods.unweightedAverage(dataset);
/* 244 */     double mean = unwtAv.getValue();
/* 245 */     double stdDev = unwtAv.getLower() * Math.sqrt(n);
/* 247 */     boolean[] isOutlier = new boolean[n];
/*     */     int i;
/* 248 */     for (i = 0; i < n; i++)
/* 249 */       isOutlier[i] = false; 
/* 252 */     boolean leaveLoop = false;
/* 253 */     int globalNumOutliers = 1;
/* 254 */     while (!leaveLoop) {
/* 255 */       leaveLoop = true;
/* 256 */       double maxNormDev = calcPeircesMaxNormDev(n, globalNumOutliers);
/* 258 */       globalNumOutliers--;
/* 259 */       int interationNumOutliers = 0;
/* 260 */       for (i = 0; i < n; i++) {
/* 261 */         if (!isOutlier[i] && Math.abs(dataset[i].getValue() - mean) / 
/* 262 */           stdDev > maxNormDev) {
/* 263 */           isOutlier[i] = true;
/* 264 */           interationNumOutliers++;
/* 265 */           globalNumOutliers++;
/*     */         } 
/*     */       } 
/* 268 */       if (interationNumOutliers > 0) {
/* 269 */         globalNumOutliers++;
/* 270 */         leaveLoop = false;
/*     */       } 
/*     */     } 
/* 274 */     List<dataPt> outliers = new ArrayList<>();
/* 275 */     dataPt[] dataPt_arr = new dataPt[0];
/* 277 */     for (i = 0; i < n; i++) {
/* 278 */       if (isOutlier[i])
/* 279 */         outliers.add(dataset[i]); 
/*     */     } 
/* 282 */     return outliers.<dataPt>toArray(dataPt_arr);
/*     */   }
/*     */   
/*     */   public static final dataPt[] ModifiedPeirceCriterion(dataPt[] dataset) {
/* 293 */     double sqrt2 = Math.sqrt(2.0D);
/* 305 */     int n = dataset.length;
/* 306 */     List<dataPt> outliers = new ArrayList<>();
/* 307 */     dataPt[] dataPt_arr = new dataPt[0];
/* 308 */     if (n == 2)
/* 309 */       return outliers.<dataPt>toArray(dataPt_arr); 
/* 312 */     dataPt wtAv = averagingMethods.weightedAverage(dataset);
/* 313 */     double mean = wtAv.getValue();
/* 315 */     double[] normDev = new double[n];
/* 316 */     List<dataPt> sortedSet = new ArrayList<>();
/*     */     int i;
/* 319 */     for (i = 0; i < n; i++)
/* 320 */       sortedSet.add(dataset[i]); 
/* 324 */     Collections.sort(sortedSet, 
/* 325 */         dataPt.normalizedDeviationComparatorConstructor(mean));
/* 328 */     for (i = 0; i < n; i++)
/* 329 */       normDev[i] = ((dataPt)sortedSet.get(i)).normalizedDeviation(mean); 
/* 332 */     boolean leaveLoop = false;
/* 333 */     int m = 1;
/* 334 */     while (!leaveLoop) {
/* 335 */       leaveLoop = true;
/* 337 */       double nmRatio = n / m;
/* 338 */       double k = m * Math.exp(nmRatio - 1.0D * Math.log((n - m)) - 
/* 339 */           nmRatio * Math.log(n));
/* 340 */       double rmax = sqrt2 * MathSpecialFunctions.inverseErf(1.0D - k);
/* 342 */       if (rmax < normDev[m - 1]) {
/* 344 */         while (rmax < normDev[m - 1] && n - m > 1) {
/* 345 */           outliers.add(sortedSet.get(m - 1));
/* 346 */           m++;
/*     */         } 
/* 348 */         leaveLoop = false;
/*     */       } 
/* 350 */       if (n - m <= 1)
/* 351 */         leaveLoop = true; 
/*     */     } 
/* 354 */     m--;
/* 355 */     return outliers.<dataPt>toArray(dataPt_arr);
/*     */   }
/*     */   
/*     */   public static final double consistantVariance(double mean, dataPt[] dataset, double p) {
/* 375 */     int n = dataset.length;
/* 376 */     double k = MathSpecialFunctions.inverseErf(2.0D * p / 100.0D - 1.0D);
/* 377 */     k *= k;
/* 379 */     double[] resultArr = new double[n];
/* 380 */     for (int i = 0; i < n; i++) {
/* 381 */       double d = mean - dataset[i].getValue();
/* 382 */       resultArr[i] = d * d / 2.0D * k - dataset[i].gaussVariance();
/*     */     } 
/* 384 */     return Arrays.stream(resultArr).max().getAsDouble();
/*     */   }
/*     */ }


/* Location:              D:\X\ND\ENSDF\AverageTool_22January2025.jar!\averagingAlgorithms\outlierMethods.class
 * Java compiler version: 8 (52.0)
 * JD-Core Version:       1.1.3
 */