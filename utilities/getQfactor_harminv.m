function Q_harminv_local = getQfactor_harminv(x, harminvDataFile, dt_mus, lambdaLow_nm, lambdaHigh_nm)
    lambdaLow_mum = lambdaLow_nm*1e-3;
    lambdaHigh_mum = lambdaHigh_nm*1e-3;
    
    [ status, lambdaH_mum, Q, outFile, err, minErrInd ] = doHarminv(harminvDataFile,dt_mus,lambdaLow_mum,lambdaHigh_mum);
    if (status == 0)
      lambdaH_nm = lambdaH_mum*1e3;
      
      rel=1./err; rel=rel/max(rel)*max(Q);
      
      [indS,val] = closestInd(lambdaH_nm,x)
      
      if length(indS)==0
        error('no closest index found!!!');
      end
      
      for i = 1:length(indS)
        idx = indS(i)
        if i == 1
          Q_harminv_local = Q(idx);
          err_last = err(idx)
        else
          if(err(idx)<err_last)
            Q_harminv_local = Q(idx);
            err_last = err(idx)
          end
        end
      end
      
      peakWaveLength_nm = x;
      Frequency_Hz = get_c0()/peakWaveLength_nm*1e9;
      
    else
      Q_harminv_local = -1;
      warning('Failed to get Q factor from harminv.');
    end
end
