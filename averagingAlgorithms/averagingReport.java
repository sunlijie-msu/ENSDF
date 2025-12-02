/*     */ package averagingAlgorithms;
/*     */ 
/*     */ import ensdf_datapoint.dataPt;
/*     */ import java.util.ArrayList;
/*     */ import java.util.Arrays;
/*     */ import java.util.List;
/*     */ import text_io.textTable;
/*     */ 
/*     */ public class averagingReport {
/*  43 */   public dataPt[] adjustedDataSet = null;
/*     */   
/*  44 */   public double criticalChiSq = -1.0D;
/*     */   
/*  45 */   public double[] differenceFromMeanSq = null;
/*     */   
/*  46 */   public dataPt[] means = null;
/*     */   
/*  47 */   public double[] normalizedResiduals = null;
/*     */   
/*  48 */   public dataPt[] originalDataSet = null;
/*     */   
/*  49 */   public dataPt[] outliers = null;
/*     */   
/*  50 */   public double[] ptChiSq = null;
/*     */   
/*  51 */   public double reducedChiSq = -1.0D;
/*     */   
/*  52 */   public double rejectionConfidence = -1.0D;
/*     */   
/*  53 */   public double[] relativeWeights = null;
/*     */   
/*     */   public boolean useUnweightedMean = false;
/*     */   
/*  55 */   public Integer[] changedPoints = null;
/*     */   
/*  56 */   public double bootstrap_NUM_MEDIANS = -1.0D;
/*     */   
/*  57 */   public double hypTest = -1.0D;
/*     */   
/*  58 */   public double[] hypTestRpt = null;
/*     */   
/*  59 */   public String dataSetName = null;
/*     */   
/*  60 */   public String methodName = null;
/*     */   
/*     */   public String methodHeader() {
/*  69 */     return "-------" + this.methodName + "-------" + "\n";
/*     */   }
/*     */   
/*     */   public String methodFooter() {
/*  79 */     String result = "";
/*  81 */     for (int i = 0; i < 14 + this.methodName.length(); i++)
/*  82 */       result = String.valueOf(result) + "-"; 
/*  84 */     return String.valueOf(result) + "\n";
/*     */   }
/*     */   
/*     */   public String dataSetHeader() {
/*  92 */     return "*******" + this.dataSetName + "*******" + "\n";
/*     */   }
/*     */   
/*     */   public String dataSetFooter() {
/* 102 */     String result = "";
/* 104 */     for (int i = 0; i < 14 + this.dataSetName.length(); i++)
/* 105 */       result = String.valueOf(result) + "*"; 
/* 107 */     return String.valueOf(result) + "\n";
/*     */   }
/*     */   
/*     */   public double minUncert() {
/* 118 */     if (this.originalDataSet.length == 0)
/* 119 */       return 0.0D; 
/* 122 */     double[] uncerts = new double[this.originalDataSet.length];
/* 124 */     for (int i = 0; i < this.originalDataSet.length; i++)
/* 125 */       uncerts[i] = Math.sqrt(this.originalDataSet[i].gaussVariance()); 
/* 127 */     return MathBasicFunction.min(uncerts);
/*     */   }
/*     */   
/*     */   public boolean isSmallerUncert(dataPt average) {
/* 139 */     boolean smallLower = true, smallUpper = true;
/* 142 */     boolean smallerUncert = true;
/* 144 */     double uncLower = average.getLower();
/* 145 */     double uncUpper = average.getUpper();
/* 146 */     for (int i = 0; i < this.originalDataSet.length; i++) {
/* 149 */       dataPt pt = this.originalDataSet[i];
/* 151 */       double uncL = pt.getLower();
/* 152 */       double uncU = pt.getUpper();
/* 153 */       if (uncLower >= uncL)
/* 154 */         smallLower = false; 
/* 155 */       if (uncUpper >= uncU)
/* 156 */         smallUpper = false; 
/* 158 */       if (!smallLower && !smallUpper) {
/* 159 */         smallerUncert = false;
/*     */         break;
/*     */       } 
/*     */     } 
/* 164 */     return smallerUncert;
/*     */   }
/*     */   
/*     */   public dataPt findSuggestedAverage(dataPt average) {
/* 173 */     dataPt suggested = null;
/* 175 */     if (this.originalDataSet.length < 2)
/* 176 */       return average; 
/* 178 */     double uncLower = average.getLower();
/* 179 */     double uncUpper = average.getUpper();
/* 181 */     dataPt pt0 = this.originalDataSet[0];
/* 182 */     double minLower = pt0.getLower();
/* 183 */     double minUpper = pt0.getUpper();
/* 184 */     if (minLower == 0.0D)
/* 185 */       minLower = 1.0E10D; 
/* 186 */     if (minUpper == 0.0D)
/* 187 */       minUpper = 1.0E10D; 
/* 189 */     for (int i = 0; i < this.originalDataSet.length; i++) {
/* 192 */       dataPt pt = this.originalDataSet[i];
/* 194 */       double uncL = pt.getLower();
/* 195 */       double uncU = pt.getUpper();
/* 196 */       if (uncL > 0.0D && uncL < minLower)
/* 197 */         minLower = uncL; 
/* 198 */       if (uncU > 0.0D && uncU < minUpper)
/* 199 */         minUpper = uncU; 
/*     */     } 
/* 202 */     if (uncLower < minLower)
/* 203 */       uncLower = minLower; 
/* 204 */     if (uncUpper < minUpper)
/* 205 */       uncUpper = minUpper; 
/* 207 */     suggested = new dataPt(average);
/* 208 */     suggested.setLower(uncLower);
/* 209 */     suggested.setUpper(uncUpper);
/* 211 */     return suggested;
/*     */   }
/*     */   
/*     */   public String briefReport(dataPt average) {
/* 227 */     if (this.dataSetName != null) {
/* 228 */       result = dataSetHeader();
/*     */     } else {
/* 230 */       result = "";
/*     */     } 
/* 232 */     if (this.methodName != null)
/* 233 */       result = String.valueOf(result) + methodHeader(); 
/* 235 */     String result = String.valueOf(result) + average.toString() + "\n";
/* 236 */     if (this.reducedChiSq > -1.0D) {
/* 237 */       result = String.valueOf(result) + "Chi^2/(N-1) = " + String.format("%1.2f", new Object[] { Double.valueOf(this.reducedChiSq) }) + "\n";
/* 238 */       if (this.criticalChiSq > -1.0D)
/* 239 */         result = String.valueOf(result) + "Critical Chi^2/(N-1) = " + String.format("%1.2f", new Object[] { Double.valueOf(this.criticalChiSq) }) + " for rejection at " + String.valueOf(this.rejectionConfidence) + 
/* 241 */           "% confidence level.\n"; 
/*     */     } 
/* 244 */     if (this.hypTest > -1.0D)
/* 245 */       result = String.valueOf(result) + "Confidence Level = " + String.format("%1.1f", new Object[] { Double.valueOf(this.hypTest * 100.0D) }) + "%.\n"; 
/* 251 */     boolean smallerUncert = isSmallerUncert(average);
/* 252 */     if (smallerUncert) {
/* 253 */       result = String.valueOf(result) + "Note: result has lower uncertainty than the smallest measured uncertainty.\n";
/* 255 */       dataPt pt = findSuggestedAverage(average);
/* 256 */       result = String.valueOf(result) + "Suggested: " + pt.toString() + "\n";
/*     */     } 
/* 259 */     if (this.methodName != null)
/* 260 */       result = String.valueOf(result) + methodFooter(); 
/* 262 */     if (this.dataSetName != null)
/* 263 */       result = String.valueOf(result) + dataSetFooter(); 
/* 266 */     return result;
/*     */   }
/*     */   
/*     */   public String briefReport() {
/* 276 */     return briefReport(this.means[0]);
/*     */   }
/*     */   
/*     */   private String doublePrint(double x) {
/* 288 */     if (Math.abs(x) < 0.01D)
/* 289 */       return String.format("%1.2e", new Object[] { Double.valueOf(x) }); 
/* 291 */     return String.format("%1.2f", new Object[] { Double.valueOf(x) });
/*     */   }
/*     */   
/*     */   public List<String> fullReport() {
/* 302 */     textTable reportData = new textTable();
/* 305 */     int n = this.originalDataSet.length;
/* 308 */     if (this.differenceFromMeanSq != null) {
/* 309 */       reportData.setCell(0, 0, "Data Point");
/* 310 */       reportData.setCell(0, 1, "(Difference from mean)**2");
/* 311 */       for (int j = 0; j < this.differenceFromMeanSq.length; j++) {
/* 312 */         reportData.setCell(j + 1, 0, this.originalDataSet[j].toString(true));
/* 313 */         reportData.setCell(j + 1, 1, doublePrint(this.differenceFromMeanSq[j]));
/*     */       } 
/* 315 */     } else if (this.normalizedResiduals != null) {
/* 316 */       reportData.setCell(0, 0, "Data Point");
/* 317 */       reportData.setCell(0, 1, "Relative Weight (%)");
/* 318 */       reportData.setCell(0, 2, "Point Chi**2");
/* 319 */       reportData.setCell(0, 3, "Normalized Residual");
/* 320 */       for (int j = 0; j < this.adjustedDataSet.length; j++) {
/* 321 */         if (Arrays.<Integer>asList(this.changedPoints).contains(Integer.valueOf(j))) {
/* 322 */           reportData.setCell(j + 1, 0, String.valueOf(this.adjustedDataSet[j].toString(true)) + "**");
/*     */         } else {
/* 324 */           reportData.setCell(j + 1, 0, this.adjustedDataSet[j].toString(true));
/*     */         } 
/* 326 */         reportData.setCell(j + 1, 1, doublePrint(this.relativeWeights[j] * 100.0D));
/* 327 */         reportData.setCell(j + 1, 2, doublePrint(this.ptChiSq[j]));
/* 328 */         reportData.setCell(j + 1, 3, doublePrint(this.normalizedResiduals[j]));
/*     */       } 
/* 330 */     } else if (this.hypTestRpt != null) {
/* 331 */       reportData.setCell(0, 0, "Data Point");
/* 332 */       reportData.setCell(0, 1, "Relative Weight (%)");
/* 333 */       for (int j = 0; j < this.originalDataSet.length; j++) {
/* 334 */         reportData.setCell(j + 1, 0, this.originalDataSet[j].toString(true));
/* 335 */         reportData.setCell(j + 1, 1, doublePrint(this.relativeWeights[j] * 100.0D));
/*     */       } 
/* 337 */     } else if (this.ptChiSq == null && !this.useUnweightedMean && this.relativeWeights != null) {
/* 338 */       reportData.setCell(0, 0, "Data Point");
/* 339 */       reportData.setCell(0, 1, "Relative Weight (%)");
/* 340 */       for (int j = 0; j < this.originalDataSet.length; j++) {
/* 341 */         reportData.setCell(j + 1, 0, this.originalDataSet[j].toString(true));
/* 342 */         reportData.setCell(j + 1, 1, doublePrint(this.relativeWeights[j] * 100.0D));
/*     */       } 
/* 344 */     } else if (this.adjustedDataSet != null) {
/* 345 */       reportData.setCell(0, 0, "Data Point");
/* 346 */       reportData.setCell(0, 1, "Relative Weight (%)");
/* 347 */       reportData.setCell(0, 2, "Point Chi**2");
/* 348 */       for (int j = 0; j < this.adjustedDataSet.length; j++) {
/* 349 */         if (this.changedPoints == null) {
/* 350 */           reportData.setCell(j + 1, 0, this.adjustedDataSet[j].toString(true));
/* 352 */         } else if (Arrays.<Integer>asList(this.changedPoints).contains(Integer.valueOf(j))) {
/* 353 */           reportData.setCell(j + 1, 0, String.valueOf(this.adjustedDataSet[j].toString(true)) + "**");
/*     */         } else {
/* 355 */           reportData.setCell(j + 1, 0, this.adjustedDataSet[j].toString(true));
/*     */         } 
/* 358 */         reportData.setCell(j + 1, 1, doublePrint(this.relativeWeights[j] * 100.0D));
/* 359 */         reportData.setCell(j + 1, 2, doublePrint(this.ptChiSq[j]));
/*     */       } 
/* 361 */     } else if (this.relativeWeights != null) {
/* 362 */       reportData.setCell(0, 0, "Data Point");
/* 363 */       reportData.setCell(0, 1, "Relative Weight (%)");
/* 364 */       reportData.setCell(0, 2, "Point Chi**2");
/* 365 */       for (int j = 0; j < this.originalDataSet.length; j++) {
/* 366 */         reportData.setCell(j + 1, 0, this.originalDataSet[j].toString(true));
/* 367 */         reportData.setCell(j + 1, 1, doublePrint(this.relativeWeights[j] * 100.0D));
/* 368 */         reportData.setCell(j + 1, 2, doublePrint(this.ptChiSq[j]));
/*     */       } 
/* 370 */     } else if (this.bootstrap_NUM_MEDIANS != -1.0D) {
/* 371 */       reportData.setCell(0, 0, "Data Point");
/* 374 */       for (int j = 0; j < this.originalDataSet.length; j++)
/* 375 */         reportData.setCell(j + 1, 0, this.originalDataSet[j].toString(true)); 
/*     */     } 
/* 381 */     List<String> result = new ArrayList<>();
/* 383 */     if (this.dataSetName != null)
/* 384 */       result.add(dataSetHeader()); 
/* 386 */     if (this.methodName != null)
/* 387 */       result.add(methodHeader()); 
/* 390 */     if (!reportData.isEmpty())
/* 391 */       for (String line : reportData.toStringList())
/* 392 */         result.add(line);  
/* 396 */     if (this.bootstrap_NUM_MEDIANS != -1.0D) {
/* 397 */       result.add("");
/* 398 */       result.add("Number of sub-sample medians taken: " + 
/* 399 */           String.valueOf((int)this.bootstrap_NUM_MEDIANS));
/* 400 */       result.add("Chi**2/(N-1): " + doublePrint(this.reducedChiSq));
/*     */     } 
/* 402 */     if (this.changedPoints != null && 
/* 403 */       this.changedPoints.length > 0)
/* 404 */       result.add("** Uncertainty adjusted"); 
/* 408 */     if (this.useUnweightedMean)
/* 409 */       result.add("LWM Adopted the unweighted average since the weighted and unwighted averages did not agree within uncertainty."); 
/* 412 */     if (this.hypTestRpt != null) {
/* 413 */       result.add("");
/* 414 */       result.add("~~Confidence Test Summary~~");
/* 415 */       result.add("Expected number of points below mean: " + 
/* 416 */           String.valueOf(Math.round(this.hypTestRpt[0] * n)));
/* 417 */       result.add("Observed number below mean: " + String.valueOf((int)this.hypTestRpt[2]));
/* 418 */       result.add("Expected number of points above mean: " + 
/* 419 */           String.valueOf(Math.round(this.hypTestRpt[1] * n)));
/* 420 */       result.add("Observed number above mean: " + String.valueOf((int)this.hypTestRpt[3]));
/* 421 */       result.add("Resulting statistic: " + String.format("%6.3f", new Object[] { Double.valueOf(this.hypTestRpt[4]) }));
/*     */     } 
/* 424 */     if (this.outliers != null) {
/* 425 */       result.add("");
/* 426 */       result.add("Points excluded as outliers:");
/* 427 */       for (int j = 0; j < this.outliers.length; j++)
/* 428 */         result.add(this.outliers[j].toString()); 
/*     */     } 
/* 432 */     result.add("");
/* 433 */     result.add("Number of input values: " + String.valueOf(this.originalDataSet.length));
/* 435 */     if (this.ptChiSq == null && !this.useUnweightedMean && this.reducedChiSq > -1.0D)
/* 436 */       result.add("Chi**2/(N-1): " + doublePrint(this.reducedChiSq)); 
/* 439 */     if (this.criticalChiSq > -1.0D) {
/* 440 */       result.add("Chi**2/(N-1): " + String.format("%1.2f", new Object[] { Double.valueOf(this.reducedChiSq) }));
/* 441 */       result.add("Critical Chi**2/(N-1): " + doublePrint(this.criticalChiSq));
/*     */     } 
/* 443 */     if (this.hypTest != -1.0D)
/* 444 */       result.add("Confidence Level: " + String.format("%1.1f", new Object[] { Double.valueOf(this.hypTest * 100.0D) }) + "%"); 
/* 448 */     result.add("");
/* 449 */     for (int i = 0; i < this.means.length; i++)
/* 450 */       result.add(this.means[i].toString()); 
/* 453 */     if (this.methodName != null)
/* 454 */       result.add(methodFooter()); 
/* 457 */     if (this.dataSetName != null)
/* 458 */       result.add(dataSetFooter()); 
/* 461 */     return result;
/*     */   }
/*     */ }


/* Location:              D:\X\ND\ENSDF\AverageTool_22January2025.jar!\averagingAlgorithms\averagingReport.class
 * Java compiler version: 8 (52.0)
 * JD-Core Version:       1.1.3
 */