/*    */ package averagingAlgorithms;
/*    */ 
/*    */ public class arrayMaxMin {
/*    */   public final double max;
/*    */   
/*    */   public final double min;
/*    */   
/*    */   public final int maxInd;
/*    */   
/*    */   public final int minInd;
/*    */   
/*    */   public arrayMaxMin(double[] a) {
/* 39 */     double maximum = a[0];
/* 40 */     double minimum = a[0];
/* 41 */     int maximumIndex = 0;
/* 42 */     int minimumIndex = 0;
/* 43 */     if (a.length > 1)
/* 44 */       for (int i = 1; i < a.length; i++) {
/* 45 */         if (a[i] > maximum) {
/* 46 */           maximum = a[i];
/* 47 */           maximumIndex = i;
/*    */         } 
/* 49 */         if (a[i] < minimum) {
/* 50 */           minimum = a[i];
/* 51 */           minimumIndex = i;
/*    */         } 
/*    */       }  
/* 55 */     this.max = maximum;
/* 56 */     this.min = minimum;
/* 57 */     this.maxInd = maximumIndex;
/* 58 */     this.minInd = minimumIndex;
/*    */   }
/*    */ }


/* Location:              D:\X\ND\ENSDF\AverageTool_22January2025.jar!\averagingAlgorithms\arrayMaxMin.class
 * Java compiler version: 8 (52.0)
 * JD-Core Version:       1.1.3
 */