; ModuleID = 'kernel_3.cpp_mem2reg_constprop_simplifycfg.ll'
source_filename = "src/kernel_3.cpp"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

; Function Attrs: noinline nounwind uwtable
define i32 @_Z8kernel_3PiS_S_S_(i32* %a, i32* %b, i32* %c, i32* %d) #0 {
entry:
  br label %for.body

for.body:                                         ; preds = %for.body, %entry
  %i.02 = phi i32 [ 0, %entry ], [ %inc, %for.body ]
  %acc.01 = phi i32 [ 0, %entry ], [ %add7, %for.body ]
  %0 = zext i32 %i.02 to i64
  %arrayidx = getelementptr inbounds i32, i32* %a, i64 %0
  %1 = load i32, i32* %arrayidx, align 4
  %2 = zext i32 %i.02 to i64
  %arrayidx2 = getelementptr inbounds i32, i32* %b, i64 %2
  %3 = load i32, i32* %arrayidx2, align 4
  %mul = mul nsw i32 %1, %3
  %4 = zext i32 %i.02 to i64
  %arrayidx4 = getelementptr inbounds i32, i32* %c, i64 %4
  %5 = load i32, i32* %arrayidx4, align 4
  %sub = sub nsw i32 %mul, %5
  %6 = zext i32 %i.02 to i64
  %arrayidx6 = getelementptr inbounds i32, i32* %d, i64 %6
  %7 = load i32, i32* %arrayidx6, align 4
  %add = add nsw i32 %sub, %7
  %add7 = add nsw i32 %acc.01, %add
  %inc = add nuw nsw i32 %i.02, 1
  %cmp = icmp ult i32 %inc, 100
  br i1 %cmp, label %for.body, label %for.end

for.end:                                          ; preds = %for.body
  ret i32 %add7
}

; Function Attrs: noinline norecurse nounwind uwtable
define i32 @main() #1 {
entry:
  %a = alloca [100 x i32], align 16
  %b = alloca [100 x i32], align 16
  %c = alloca [100 x i32], align 16
  %d = alloca [100 x i32], align 16
  br label %for.body

for.body:                                         ; preds = %for.body, %entry
  %i.01 = phi i32 [ 0, %entry ], [ %inc, %for.body ]
  %call = call i32 @rand() #3
  %rem = srem i32 %call, 10
  %0 = zext i32 %i.01 to i64
  %arrayidx = getelementptr inbounds [100 x i32], [100 x i32]* %a, i64 0, i64 %0
  store i32 %rem, i32* %arrayidx, align 4
  %call1 = call i32 @rand() #3
  %rem2 = srem i32 %call1, 10
  %1 = zext i32 %i.01 to i64
  %arrayidx4 = getelementptr inbounds [100 x i32], [100 x i32]* %b, i64 0, i64 %1
  store i32 %rem2, i32* %arrayidx4, align 4
  %call5 = call i32 @rand() #3
  %rem6 = srem i32 %call5, 10
  %2 = zext i32 %i.01 to i64
  %arrayidx8 = getelementptr inbounds [100 x i32], [100 x i32]* %c, i64 0, i64 %2
  store i32 %rem6, i32* %arrayidx8, align 4
  %call9 = call i32 @rand() #3
  %rem10 = srem i32 %call9, 10
  %3 = zext i32 %i.01 to i64
  %arrayidx12 = getelementptr inbounds [100 x i32], [100 x i32]* %d, i64 0, i64 %3
  store i32 %rem10, i32* %arrayidx12, align 4
  %inc = add nuw nsw i32 %i.01, 1
  %cmp = icmp ult i32 %inc, 100
  br i1 %cmp, label %for.body, label %for.end

for.end:                                          ; preds = %for.body
  %arraydecay = getelementptr inbounds [100 x i32], [100 x i32]* %a, i64 0, i64 0
  %arraydecay13 = getelementptr inbounds [100 x i32], [100 x i32]* %b, i64 0, i64 0
  %arraydecay14 = getelementptr inbounds [100 x i32], [100 x i32]* %c, i64 0, i64 0
  %arraydecay15 = getelementptr inbounds [100 x i32], [100 x i32]* %d, i64 0, i64 0
  %call16 = call i32 @_Z8kernel_3PiS_S_S_(i32* nonnull %arraydecay, i32* nonnull %arraydecay13, i32* nonnull %arraydecay14, i32* nonnull %arraydecay15)
  ret i32 0
}

; Function Attrs: nounwind
declare i32 @rand() #2

attributes #0 = { noinline nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { noinline norecurse nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 6.0.1 (http://github.com/llvm-mirror/clang 2f27999df400d17b33cdd412fdd606a88208dfcc) (http://github.com/llvm-mirror/llvm 5136df4d089a086b70d452160ad5451861269498)"}
